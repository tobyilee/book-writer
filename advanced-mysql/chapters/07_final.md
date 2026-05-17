# 7장. JSON 데이터 모델링과 인덱싱

상품 상세 정보를 저장한다고 해보자. 의류는 색상, 사이즈, 소재가 있고, 전자제품은 해상도, 배터리 용량, 운영체제 버전이 있고, 식품은 원산지, 알레르기 성분, 영양 성분이 있다. 카테고리마다 속성이 다르다. 관계형 테이블로 다 잡으려면 모든 카테고리의 속성을 합친 거대한 테이블을 만들어야 하거나, 속성 이름과 값을 행으로 저장하는 EAV(Entity-Attribute-Value) 패턴을 써야 하는데 이것도 번거롭긴 마찬가지다.

이때 JSON 컬럼이 매력적으로 보인다. `attributes` 컬럼 하나에 카테고리마다 다른 속성들을 자유롭게 담는 것이다. 문제는 "그래서 이 JSON 컬럼에서 특정 값을 빠르게 찾을 수 있느냐"다.

MySQL 8.0은 이 문제에 구체적인 답을 내놓았다.

## JSON 타입과 기본 사용법

MySQL 5.7부터 JSON이 네이티브 타입으로 들어왔다. 텍스트 컬럼에 JSON 문자열을 저장하는 것과는 다르다. JSON 타입으로 저장하면 MySQL이 파싱해서 최적화된 내부 이진 형식으로 보관한다. 덕분에 JSON 문서 안의 특정 경로를 직접 접근하는 것이 빠르고, 저장 시 문법 유효성 검사도 자동으로 된다.

```sql
-- JSON 컬럼을 포함한 테이블 생성
CREATE TABLE products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL,
    attributes JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- JSON 데이터 삽입
INSERT INTO products (name, category_id, attributes) VALUES
('청바지 스키니핏', 1,
 '{"color": "dark_blue", "sizes": ["S", "M", "L", "XL"], "material": "cotton_96"}'),
('갤럭시 S24', 2,
 '{"storage": 256, "ram": 8, "os": "Android14", "battery_mAh": 4000}');
```

### JSON_EXTRACT와 `->>` 연산자

JSON 안의 값을 꺼내는 방법이 여럿 있다.

```sql
-- JSON_EXTRACT 함수: JSON 경로로 값 추출
SELECT name,
       JSON_EXTRACT(attributes, '$.color') AS color,
       JSON_EXTRACT(attributes, '$.storage') AS storage
FROM products;

-- ->> 연산자: JSON_UNQUOTE(JSON_EXTRACT()) 의 짧은 표현
-- 문자열 값에서 따옴표를 제거해 순수 값으로 반환
SELECT name,
       attributes->>'$.color' AS color,
       attributes->>'$.storage' AS storage
FROM products;

-- 배열 인덱스로 접근
SELECT name, attributes->>'$.sizes[0]' AS first_size
FROM products
WHERE category_id = 1;

-- 조건 검색
SELECT * FROM products
WHERE attributes->>'$.storage' = '256';
```

`->`는 JSON 경로로 값을 추출하되 따옴표가 붙고, `->>`는 따옴표를 제거한 순수 값을 반환한다. 숫자를 다룰 때는 `->>`를 쓰는 편이 낫다. 그렇지 않으면 `"256"` 같은 따옴표 달린 문자열로 반환되어 비교가 찜찜해진다.

### JSON_TABLE로 JSON을 관계형으로 펼치기

JSON 안의 배열 데이터를 행으로 펼쳐서 일반 테이블처럼 다루고 싶을 때가 있다.

```sql
-- JSON 배열을 행으로 변환
SELECT p.name, sizes.size
FROM products p,
JSON_TABLE(
    p.attributes,
    '$.sizes[*]' COLUMNS (
        size VARCHAR(10) PATH '$'
    )
) AS sizes
WHERE p.category_id = 1;
```

결과는 `청바지 스키니핏 | S`, `청바지 스키니핏 | M` 같이 배열 요소마다 한 행으로 펼쳐진다. JSON_TABLE을 쓰면 JSON 데이터를 관계형 JOIN이나 GROUP BY와 함께 쓸 수 있다. 다만 내부적으로 임시 테이블을 만드는 방식이라 대용량에서는 부담이 될 수 있다.

## JSON 인덱싱 — 5.7초에서 280ms로

JSON 컬럼 자체에는 인덱스를 직접 걸 수 없다. `CREATE INDEX idx ON products (attributes)` 같은 것은 허용되지 않는다. JSON 문서 전체에 B+Tree 인덱스를 만드는 것 자체가 말이 안 되기 때문이다.

대신 JSON 안의 특정 경로 값을 인덱싱하는 방법이 있다.

### MySQL 5.7 방식: 생성 컬럼 + 세컨더리 인덱스

```sql
-- generated column으로 JSON 경로를 일반 컬럼으로 추출
ALTER TABLE products
ADD COLUMN storage_gb INT GENERATED ALWAYS AS
    (CAST(attributes->>'$.storage' AS UNSIGNED)) VIRTUAL;

-- 그 generated column에 인덱스 생성
ALTER TABLE products
ADD INDEX idx_storage (storage_gb);

-- 이제 이 쿼리가 인덱스를 탄다
SELECT * FROM products WHERE storage_gb = 256;
-- 또는 JSON 경로 조건도 MySQL이 자동으로 인덱스 활용
SELECT * FROM products WHERE attributes->>'$.storage' = '256';
```

VIRTUAL 생성 컬럼은 디스크에 값을 저장하지 않고 조회 시점에 계산한다. 인덱스는 그 계산된 값을 기반으로 만들어진다. 이 방식이 MySQL 5.7에서의 우회 패턴이었다.

### MySQL 8.0.13 이상: 함수형 인덱스

8.0.13부터는 생성 컬럼 없이 바로 인덱스를 정의할 수 있다. 내부적으로는 같은 원리지만 테이블 구조를 건드리지 않아도 된다.

```sql
-- 8.0.13+ 함수형 인덱스
ALTER TABLE products
ADD INDEX idx_storage ((CAST(attributes->>'$.storage' AS UNSIGNED)));
```

```sql
-- EXPLAIN으로 인덱스 활용 확인
EXPLAIN SELECT * FROM products
WHERE (CAST(attributes->>'$.storage' AS UNSIGNED)) = 256;
```

`EXPLAIN`에서 `key: idx_storage`가 보이면 인덱스를 타고 있는 것이다.

1mg(인도 헬스케어 플랫폼)의 사례가 이 효과를 잘 보여준다. 의약품 데이터의 특정 속성을 JSON 컬럼에 저장하고 있었는데, 그 속성으로 검색하는 쿼리가 5.7초가 걸렸다. VIRTUAL 생성 컬럼에 세컨더리 인덱스를 추가한 결과 280ms로 줄었다. 약 20배 개선이다. 8.0.21 이후라면 함수형 인덱스로 같은 효과를 생성 컬럼 없이 낼 수 있다.

여기서 핵심은 JSON 경로와 인덱스 정의의 표현식이 정확히 일치해야 한다는 것이다. `attributes->>'$.storage'`와 `JSON_EXTRACT(attributes, '$.storage')`는 같은 값이지만 인덱스가 어떤 표현식으로 정의됐는지에 따라 둘 중 하나만 인덱스를 탄다. EXPLAIN으로 확인해두는 편이 낫다.

## JSON vs 정규화 — 경계선은 어디인가

JSON 컬럼을 쓰자, 아니다 정규화 테이블이 낫다 — 팀 안에서 한 번쯤 부딪히는 논쟁이다. 정해진 답은 없지만 판단 기준은 있다.

JSON이 어울리는 상황부터 보자. 속성이 카테고리마다 크게 다르고 공통 스키마를 강제하기 어려운 경우. 속성이 자주 바뀌거나 신규 속성 추가가 빈번한 경우(스키마 변경 없이 새 키를 더할 수 있다). 검색·정렬·집계 대상이 되는 속성이 전체의 일부에 불과한 경우(그 속성만 인덱싱해두면 된다). 또는 사용자 설정, 이벤트 메타데이터처럼 문서 지향적인 데이터.

반면 정규화 테이블이 어울리는 상황은 다르다. 해당 컬럼을 기준으로 자주 JOIN하고 집계하고 필터링해야 할 때. 데이터 정합성이 중요하고 FK 제약이나 NOT NULL 제약이 필요할 때. 모든 행이 같은 속성 구조를 가질 때. 이런 데이터라면 JSON에 담을 이유가 없다.

```sql
-- 이렇게 자주 조인하고 집계한다면 정규화 테이블이 낫다
SELECT s.name, COUNT(*) AS product_count
FROM products p
JOIN product_specifications ps ON p.id = ps.product_id
JOIN specifications s ON ps.spec_id = s.id
GROUP BY s.name;

-- JSON으로는 이런 쿼리가 쉽지 않다
SELECT attributes->>'$.color' AS color, COUNT(*)
FROM products
GROUP BY attributes->>'$.color';
-- 이것도 가능하지만 인덱스를 타지 않아 전체 스캔이다
```

하이브리드 접근도 흔하다. 모든 상품에 공통인 속성(이름, 카테고리, 가격, 재고)은 정규화 컬럼으로, 카테고리마다 다른 세부 속성은 JSON 컬럼으로. 자주 검색되는 JSON 속성에만 함수형 인덱스를 추가한다. 이렇게 하면 스키마 유연성과 인덱싱 성능을 같이 챙길 수 있다.

## 마무리

JSON 타입은 관계형 모델의 경직성을 보완하는 도구다. 하지만 도구에는 적합한 용도가 있다. JSON 컬럼에 저장한 데이터를 자주 검색한다면 함수형 인덱스를 추가하는 편이 낫고, 정의한 표현식과 쿼리의 표현식이 정확히 일치해야 인덱스를 탄다는 것을 기억해두자. JSON을 쓸지 정규화를 쓸지의 판단 기준은 "이 데이터를 어떻게 조회하고 필터링할 것인가"에서 나온다.

8장에서는 도메인 모델링과 스키마 설계가 만나는 지점을 본다. DDD의 애그리거트를 테이블로 옮길 때 PK 전략, soft delete, 이력 관리, FK 경계에서 어떤 트레이드오프가 생기는지를 함께 살펴보자.

## 참고 자료

- MySQL :: 13.5 The JSON Data Type — https://dev.mysql.com/doc/refman/8.0/en/json.html
- MySQL :: 15.1.20.9 Secondary Indexes and Generated Columns — https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html
- MySQL :: Indexing JSON documents via Virtual Columns — https://dev.mysql.com/blog-archive/indexing-json-documents-via-virtual-columns/
- Vlad Mihalcea — Index JSON columns in MySQL — https://vladmihalcea.com/index-json-columns-mysql/
- Medium "1mg JSON support virtual columns and indexing" — https://medium.com/1mgofficial/mysql-json-support-virtual-columns-and-indexing-json-31df4cc1aa31
