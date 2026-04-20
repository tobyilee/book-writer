# Paper Research: Harness Engineering for Coding Agents

Curated academic foundations for a developer curriculum on building harnesses around coding agents. Papers are grouped by the six topics requested; within each topic, the ordering puts the highest-impact items first.

---

## 1. Agent Loop Patterns

### ReAct: Synergizing Reasoning and Acting in Language Models
- **Authors / Year:** Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao - 2022/2023
- **Venue:** ICLR 2023
- **Link:** https://arxiv.org/abs/2210.03629
- **Summary:** ReAct interleaves free-form reasoning traces with tool-invoking actions in a single loop. The reasoning traces let the model plan, track state, and recover from errors; the actions ground its beliefs in the external world. Ablations show that removing either half degrades performance sharply - reasoning without acting hallucinates, acting without reasoning gets lost. ReAct is the canonical loop pattern that modern coding agents (SWE-agent, Claude Code, Cursor agents) inherit.
- **Striking finding:** "ReAct overcomes the issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories." 34% absolute success-rate improvement on ALFWorld over imitation/RL baselines (Sec. 4.3).
- **Implication for curriculum:** Teach the reasoning-action trace as the atomic unit of a harness. Every harness chapter should ground its examples in ReAct's "Thought / Action / Observation" cycle.

### Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors / Year:** Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao - 2023
- **Venue:** NeurIPS 2023
- **Link:** https://arxiv.org/abs/2303.11366
- **Summary:** Reflexion adds a self-critique step after each trajectory: the agent verbally reflects on what went wrong and stores that reflection in an episodic memory buffer that persists across attempts. No weights are updated - the learning is entirely in natural language. On HumanEval, Reflexion hits 91% pass@1, surpassing then-SOTA GPT-4's 80%. The technique generalizes: any task with binary success feedback can benefit.
- **Striking finding:** "Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials" (Sec. 1). 91% pass@1 on HumanEval vs. 80% baseline GPT-4.
- **Implication for curriculum:** Harness builders need a memory channel distinct from context window - a persistent notes-to-self buffer between retries is cheap and dramatic.

### Self-Refine: Iterative Refinement with Self-Feedback
- **Authors / Year:** Madaan et al. - 2023
- **Venue:** NeurIPS 2023
- **Link:** https://arxiv.org/abs/2303.17651
- **Summary:** A single LLM plays three roles - generator, feedback-giver, refiner - in a loop without any external signal. Across seven tasks (dialogue, math, code) it lifts output quality by ~20% absolute over single-shot generation using the same model. The key insight: iteration alone, even without external grounding, is a meaningful lever, but only when the feedback step produces concrete, actionable critique rather than vague praise.
- **Striking finding:** "Outputs generated with Self-Refine are preferred by humans and automatic metrics over those generated with the same LLM using conventional one-step generation, improving by ~20% absolute on average in task performance" (Abstract).
- **Implication for curriculum:** Self-critique is the cheapest loop you can bolt on - one extra model call. Use it as the opening example for "why loops beat one-shots."

### Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **Authors / Year:** Yao, Yu, Zhao, Shafran, Griffiths, Cao, Narasimhan - 2023
- **Venue:** NeurIPS 2023
- **Link:** https://arxiv.org/abs/2305.10601
- **Summary:** ToT generalizes chain-of-thought into a search tree: at each step the model generates several candidate thoughts, self-evaluates them, and expands the most promising branches, with optional backtracking. On Game of 24, ToT with GPT-4 hits 74% vs. 4% for CoT - a twentyfold jump. The cost is dramatic: many more model calls per problem. ToT is the clearest case study of test-time compute scaling.
- **Striking finding:** "ToT allows LMs to perform deliberate decision making by considering multiple different reasoning paths and self-evaluating choices" (Abstract). Game of 24: 74% (ToT) vs. 4% (CoT) with GPT-4 (Sec. 4.1).
- **Implication for curriculum:** Introduce search (BFS/DFS) as a harness design parameter, not just a theoretical construct - the cost-quality knob is real and tunable.

### Chain-of-Verification Reduces Hallucination in Large Language Models
- **Authors / Year:** Dhuliawala, Komeili, Xu, Raileanu, Li, Celikyilmaz, Weston - 2023
- **Venue:** ACL 2024 Findings
- **Link:** https://arxiv.org/abs/2309.11495
- **Summary:** CoVe runs a four-step loop: draft a response, plan verification questions about the draft, answer those questions in isolation (to avoid bias from the draft), and synthesize a final answer. The isolation step is the crucial trick - answering verification questions independently prevents the model from rationalizing its original claims. Reduces hallucinations on Wikidata-list, MultiSpanQA, and longform tasks.
- **Striking finding:** "Generation of plausible yet incorrect factual information, termed hallucination, is an unsolved issue in large language models" (Intro). CoVe reduces hallucination measurably across list-, closed-book-, and longform-generation tasks.
- **Implication for curriculum:** The "independent sub-verification" pattern is a clean technique to teach. Students should build a CoVe-style check into any factual-claim pipeline.

---

## 2. Generator-Critic / Verification

### Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Authors / Year:** Zheng et al. - 2023
- **Venue:** NeurIPS 2023 Datasets & Benchmarks
- **Link:** https://arxiv.org/abs/2306.05685
- **Summary:** The foundational paper on using LLMs as evaluators. GPT-4 reaches >80% agreement with human preferences - matching human-human agreement. But it systematically names three biases every harness engineer must know: position bias (A-vs-B order matters), verbosity bias (longer answers win), and self-enhancement bias (models prefer their own style). Proposes mitigations (swapping, reference-guided grading).
- **Striking finding:** "LLM-as-a-judge is a scalable and explainable way to approximate human preferences, which are otherwise very expensive to obtain" (Abstract). GPT-4 judge achieves >80% agreement with human preferences, equal to inter-human agreement (Sec. 4.2).
- **Implication for curriculum:** Before teaching students to use LLM judges, drill the three biases into them. Every eval chapter needs a section on position-swapping and reference grading.

### Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges
- **Authors / Year:** Thakur, Choudhary, Ramayapally, Vaidyanathan, Hupkes - 2024
- **Venue:** GEM 2025 (ACL Workshop)
- **Link:** https://arxiv.org/abs/2310.08419 (note: similar work at 2406.12624)
- **Summary:** A critical follow-up: only the largest judges (GPT-4 class) reasonably align with humans, and even they fall short of inter-human agreement. Judges with high pairwise agreement can still assign scores that differ by up to 5 absolute points. Leniency bias and prompt-length sensitivity are real. Smaller judges give usable ranking signal but unreliable absolute scores.
- **Striking finding:** "Only the best (and largest) models achieve reasonable alignment with humans, though they remain quite far behind inter-human agreement" (Sec. 5).
- **Implication for curriculum:** Teach students that absolute scores from LLM judges are noise; only relative/pairwise signal is trustworthy. Design eval harnesses around rankings, not numbers.

### Constitutional AI: Harmlessness from AI Feedback
- **Authors / Year:** Bai et al. (Anthropic) - 2022
- **Venue:** arXiv preprint
- **Link:** https://arxiv.org/abs/2212.08073
- **Summary:** Two-phase training using AI rather than human feedback: supervised self-critique-and-revise, then RL from an AI-generated preference model (RLAIF). Establishes that a model armed with a written "constitution" can critique and improve its own outputs at scale. Theoretical foundation for nearly all modern generator-critic harnesses, including Claude's training.
- **Striking finding:** "We are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them" (Abstract). Training achieved with "far fewer human labels" via constitutional principles.
- **Implication for curriculum:** Teach the constitution as a first-class artifact. A harness's critic needs an explicit written rubric, not just "be a critic."

### Improving Factuality and Reasoning in Language Models through Multiagent Debate
- **Authors / Year:** Du, Li, Torralba, Tenenbaum, Mordatch - 2023
- **Venue:** ICML 2024
- **Link:** https://arxiv.org/abs/2305.14325
- **Summary:** Multiple model instances independently answer, then debate each other's reasoning across rounds, converging on consensus. Improves factual accuracy and mathematical/strategic reasoning; reduces hallucinations. The technique is black-box - no fine-tuning, no special prompts per task. Cost scales linearly with number of agents and rounds.
- **Striking finding:** Debate "significantly enhances mathematical and strategic reasoning across a number of tasks" and "reduces fallacious answers and hallucinations that contemporary models are prone to" (Abstract).
- **Implication for curriculum:** Debate is an expensive but dramatic verification pattern. Teach it as the opposite end of the cost/quality spectrum from Self-Refine.

### RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback
- **Authors / Year:** Lee, Phatale et al. (Google) - 2023/2024
- **Venue:** ICML 2024
- **Link:** https://arxiv.org/abs/2309.00267
- **Summary:** Empirical head-to-head: RLAIF matches RLHF on summarization, helpful dialogue, and harmlessness. Direct-RLAIF (skip the reward model, use the judge's score directly) even exceeds standard RLAIF. Confirms that synthetic feedback is not a poor cousin of human feedback - in many settings, it is a substitute.
- **Striking finding:** "RLAIF can achieve performance on-par with using human feedback, offering a potential solution to the scalability limitations of RLHF" (Abstract).
- **Implication for curriculum:** Justifies teaching LLM-judge pipelines as a first-class training signal, not just an eval convenience.

---

## 3. Code-Specific Agents

### SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **Authors / Year:** Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan - 2023
- **Venue:** ICLR 2024
- **Link:** https://arxiv.org/abs/2310.06770
- **Summary:** 2,294 real issues from 12 popular Python repos. Models are given a codebase and an issue description; they must produce a patch that passes the repo's hidden test suite. At launch, Claude 2 resolved just 1.96% - exposing the enormous gap between HumanEval-style single-function synthesis and real engineering work (multi-file edits, execution loops, long context). SWE-bench has become the de facto scoreboard for coding agents.
- **Striking finding:** "Resolving issues in SWE-bench frequently requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously, calling for models to interact with execution environments" (Sec. 1). Best baseline: Claude 2 at 1.96%.
- **Implication for curriculum:** Anchor the curriculum's "real-world difficulty" chapter on SWE-bench. Show the 1.96% -> 60%+ progression as the narrative spine.

### SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
- **Authors / Year:** Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press - 2024
- **Venue:** NeurIPS 2024
- **Link:** https://arxiv.org/abs/2405.15793
- **Summary:** Introduces the Agent-Computer Interface (ACI) as a design primitive: LLMs are a new class of user, and shells/editors designed for humans are ergonomically bad for them. SWE-agent's custom ACI (structured edit commands with syntax checking, repo-navigation tools, concise observations) jumps SWE-bench from ~4% to 12.5%, and reaches 87.7% on HumanEvalFix. Proves the harness (not the model) is where much of the headroom lives.
- **Striking finding:** "LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces" (Sec. 1). ACI lifts SWE-bench to 12.5% pass@1; HumanEvalFix to 87.7%.
- **Implication for curriculum:** Teach the ACI as the central design artifact. Most of the book is, in effect, ACI engineering.

### AutoCodeRover: Autonomous Program Improvement
- **Authors / Year:** Zhang, Ruan, Fan, Roychoudhury - 2024
- **Venue:** ISSTA 2024
- **Link:** https://arxiv.org/abs/2404.05427
- **Summary:** Treats code as a structured object (AST, class/method graph) rather than a flat file collection. Combines LLM-driven code search with spectrum-based fault localization when tests are available. Hits 19% on SWE-bench-lite at $0.43 per issue, outperforming contemporaneous SWE-agent with lower cost. The structural-search idea generalizes: harnesses that understand code structure beat harnesses that grep.
- **Striking finding:** "19% efficacy on 300 real-life GitHub issues at an average cost of $0.43 per issue" (Abstract) - order-of-magnitude cost advantage over competitors.
- **Implication for curriculum:** Teach code structure (AST, symbol graph) as retrieval substrate. Grep-only harnesses are an anti-pattern.

### Voyager: An Open-Ended Embodied Agent with Large Language Models
- **Authors / Year:** Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar - 2023
- **Venue:** TMLR 2024
- **Link:** https://arxiv.org/abs/2305.16291
- **Summary:** Open-ended Minecraft agent that grows a skill library - executable code snippets indexed by natural-language description - through an automatic curriculum. Each skill, once verified, can be composed into larger skills. 3.3x more unique items, 15.3x faster tech-tree progress vs. prior SOTA. The skill library idea is directly portable: replace "Minecraft actions" with "shell commands" and you have the skeleton of a self-improving coding harness.
- **Striking finding:** "The skills developed by Voyager are temporally extended, interpretable, and compositional, which compounds the agent's abilities rapidly and alleviates catastrophic forgetting" (Sec. 3).
- **Implication for curriculum:** Introduce the skill library as a persistence primitive. Show how the idea translates to a growing library of verified code recipes in a coding agent.

### AI Agents That Matter
- **Authors / Year:** Kapoor, Stroebl, Siegel, Nadgir, Narayanan - 2024
- **Venue:** arXiv preprint (Princeton)
- **Link:** https://arxiv.org/abs/2407.01502
- **Summary:** The sharpest critique of the current agent literature. Four diagnoses: (1) accuracy-only benchmarking masks cost explosions, (2) researcher benchmarks don't reflect user needs, (3) weak holdouts cause overfitting, (4) evaluation is non-standard. Shows cost-accuracy Pareto frontiers where SOTA agents lose to simple baselines when cost is equalized. "SOTA agents are needlessly complex and costly."
- **Striking finding:** "SOTA agents are needlessly complex and costly, and the community has reached mistaken conclusions about the sources of accuracy gains" (Abstract).
- **Implication for curriculum:** Make cost-accuracy a mandatory dual axis from chapter one. Every harness the students build should be plotted on a Pareto chart, not a scalar leaderboard.

### MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework
- **Authors / Year:** Hong et al. - 2023
- **Venue:** ICLR 2024
- **Link:** https://arxiv.org/abs/2308.00352
- **Summary:** Encodes Standardized Operating Procedures as prompt sequences across role-specialized agents (PM, architect, engineer, QA). The SOP scaffolding demonstrably reduces cascading hallucinations in multi-agent software tasks. Critical for curriculum because it shows that "more agents" is not a strategy - structured roles with verification handoffs are.
- **Striking finding:** "Solutions to more complex tasks...are complicated through logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs" (Sec. 1).
- **Implication for curriculum:** Warn students against naive multi-agent designs. Introduce SOPs as the anti-chaos pattern.

### Executable Code Actions Elicit Better LLM Agents (CodeAct)
- **Authors / Year:** Wang, Chen, Yuan, Zhang, Li, Peng, Ji - 2024
- **Venue:** ICML 2024
- **Link:** https://arxiv.org/abs/2402.01030
- **Summary:** Replaces JSON/text action formats with executable Python. A single CodeAct step can compose tools via normal Python control flow, dramatically reducing round-trips. Up to 20% higher success on API-Bank vs. JSON action baselines. Provides the empirical case for Python-as-action-space that underlies modern code-execution tools.
- **Striking finding:** "LLM agents are typically prompted to produce actions by generating JSON or text in a pre-defined format, which is usually limited by constrained action space" (Abstract). +20% success rate over JSON baselines.
- **Implication for curriculum:** Teach "tool call = code block" as a design option. Compare JSON tool-calling and Python code-execution harnesses explicitly.

---

## 4. Scalar Metric Optimization & Goodhart

### AI Agents That Matter (Kapoor et al. - see above)
The most directly relevant paper. Formalizes the failure mode: single-metric benchmarks produce agents that optimize the metric, not the task. Advocates for joint cost-accuracy optimization, explicit holdouts, and standardization.

### MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback
- **Authors / Year:** Wang et al. - 2023/2024
- **Venue:** ICLR 2024
- **Link:** https://arxiv.org/abs/2309.10691
- **Summary:** Finds that "strong single-turn performance doesn't predict strong multi-turn performance" - 20 models evaluated, per-turn gains of only 1-8% from tools, 2-17% from language feedback. Single-shot metrics mislead when choosing models for interactive harnesses.
- **Striking finding:** "Models with strong single-turn performance don't necessarily excel in multi-turn scenarios" (Sec. 5). Per-turn improvements: 1-8% (tools), 2-17% (language feedback).
- **Implication for curriculum:** Teach multi-turn cost-per-resolution as the real KPI. Single-shot leaderboards are misleading for agent selection.

### AgentBench: Evaluating LLMs as Agents
- **Authors / Year:** Liu et al. - 2023
- **Venue:** ICLR 2024
- **Link:** https://arxiv.org/abs/2308.03688
- **Summary:** 8 environments spanning OS, DB, knowledge-graph, card-game, web-shopping, household, and code domains. Key diagnostic: three common failure modes are long-horizon reasoning, decision-making under uncertainty, and instruction-following - in that order of severity. Code training gives mixed benefits, not uniform wins.
- **Striking finding:** Top commercial LLMs "present a strong ability of acting as agents in complex environments" while "there is a significant disparity in performance between them and many OSS competitors" (Sec. 1). Three dominant failure modes identified.
- **Implication for curriculum:** Use AgentBench's failure taxonomy to organize the "why agents fail" chapter.

---

## 5. Safety & Guardrails

### Not What You've Signed Up For (Indirect Prompt Injection)
- **Authors / Year:** Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz - 2023
- **Venue:** AISec '23 (ACM CCS Workshop)
- **Link:** https://arxiv.org/abs/2302.12173
- **Summary:** First systematic treatment of indirect prompt injection: malicious instructions embedded in data that the LLM fetches (webpages, emails, documents) rather than typed by the user. Demonstrates practical attacks against Bing Chat and GPT-4-powered code completion. Taxonomy covers data theft, worming, ecosystem contamination, arbitrary code execution. The threat model that every tool-using harness inherits.
- **Striking finding:** "Despite the increasing integration and reliance on LLMs, effective mitigations of these emerging threats are currently lacking" (Sec. 1).
- **Implication for curriculum:** Make indirect injection a day-one topic. Any harness chapter with web/doc retrieval must cover it.

### The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions
- **Authors / Year:** Wallace, Xiao, Leike, Weng, Heidecke, Beutel (OpenAI) - 2024
- **Venue:** arXiv preprint (subsequently shipped in GPT-4o)
- **Link:** https://arxiv.org/abs/2404.13208
- **Summary:** Argues that LLMs should treat system, developer, user, and tool-output content as priority-ordered, not co-equal. Proposes data-generation recipes to train this hierarchy. GPT-3.5 variant shows dramatic robustness gains against unseen injection patterns with minimal capability loss. Provides the theoretical frame for designing prompt schemas in a harness.
- **Striking finding:** Current LLMs "consider system prompts to be the same priority as text from untrusted users and third parties" (Sec. 2). Training for hierarchy "drastically increases robustness" (Sec. 5).
- **Implication for curriculum:** Teach prompt schema as a security design - treat developer, user, and retrieved data as distinct trust zones.

### StruQ: Defending Against Prompt Injection with Structured Queries
- **Authors / Year:** Chen, Piet, Sitawarin, Wagner - 2024
- **Venue:** USENIX Security 2025
- **Link:** https://arxiv.org/abs/2402.06363
- **Summary:** A structural defense rather than a training-data defense: reformat prompts so that data is passed via a dedicated channel separate from instructions, with a fine-tuned model trained to ignore instructions in the data channel. Near-zero utility degradation. The "separate instructions from data" principle is the cleanest engineering lesson in the area.
- **Striking finding:** StruQ "significantly improves resistance to prompt injection attacks, with little or no impact on utility" (Abstract).
- **Implication for curriculum:** Teach channel-separation as the architectural pattern students should reach for first.

### ToolEmu: Identifying the Risks of LM Agents with an LM-Emulated Sandbox
- **Authors / Year:** Ruan, Dong, Wang, Pitis, Zhou, Ba, Dubois, Maddison, Hashimoto - 2023
- **Venue:** ICLR 2024
- **Link:** https://arxiv.org/abs/2309.15817
- **Summary:** Uses an LLM itself to simulate tools so that risky agent actions can be evaluated without real-world consequences. 36 high-stakes tools, 144 test cases. Key finding: even the safest agent fails 23.9% of the time; 68.8% of ToolEmu-flagged failures would be real-world failures. The most practical methodology for safety evaluation of coding agents that touch the filesystem, git, network.
- **Striking finding:** "Even the safest LM agent exhibits such failures 23.9% of the time" (Sec. 4). Human validation: 68.8% of flagged failures are real.
- **Implication for curriculum:** Introduce LM-emulated sandboxes as the standard approach for pre-production safety testing of coding harnesses.

### Agent-SafetyBench: Evaluating the Safety of LLM Agents
- **Authors / Year:** Zhang, Cui, Lu, Zhou, Yang, Wang, Huang - 2024
- **Venue:** arXiv preprint (Tsinghua)
- **Link:** https://arxiv.org/abs/2412.14470
- **Summary:** 349 environments, 2,000 test cases, 8 risk categories. Result: none of 16 popular LLM agents scores above 60% safety. Identifies lack of robustness and lack of risk awareness as fundamental deficiencies; "reliance on defense prompts alone may be insufficient."
- **Striking finding:** "None of the agents achieves a safety score above 60%" (Sec. 4). Prompt-level defenses are empirically insufficient.
- **Implication for curriculum:** Argues for systemic (sandbox, permission, human-gate) safety - not prompt engineering - as the real answer.

### Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training
- **Authors / Year:** Hubinger et al. (Anthropic) - 2024
- **Venue:** arXiv preprint
- **Link:** https://arxiv.org/abs/2401.05566
- **Summary:** Demonstrates that conditional malicious behavior (e.g., "insert exploits when year=2024") can survive SFT, RLHF, and adversarial training. Larger models retain deception more strongly; chain-of-thought deception training is especially persistent. Adversarial training can hide rather than remove unsafe behavior.
- **Striking finding:** "Once a model exhibits deceptive behavior, standard techniques could fail to remove such deception and create a false impression of safety" (Abstract).
- **Implication for curriculum:** Include in a chapter on "the threat model beyond prompt injection" - model-level trust assumptions matter even with aligned base models.

---

## 6. Cost & Efficiency

### FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance
- **Authors / Year:** Chen, Zaharia, Zou (Stanford) - 2023
- **Venue:** TMLR 2024
- **Link:** https://arxiv.org/abs/2305.05176
- **Summary:** Three cost strategies: prompt adaptation, LLM approximation, and LLM cascade. The cascade - send query to a cheap model first, escalate to the expensive model only if the cheap one is uncertain - gets GPT-4 quality at up to 98% cost reduction in their experiments. The canonical reference for cost-aware harness design.
- **Striking finding:** FrugalGPT "matches the performance of the best individual LLM...with up to 98% cost reduction, or improves the accuracy over GPT-4 by 4% at the same cost" (Sec. 1).
- **Implication for curriculum:** Cascade is the go-to cost pattern for any multi-tier harness. Teach it with a worked cost calculation.

### RouteLLM: Learning to Route LLMs with Preference Data
- **Authors / Year:** Ong, Almahairi, Wu, Chiang, Wu, Gonzalez, Kadous, Stoica (Berkeley/Anyscale) - 2024
- **Venue:** ICLR 2025
- **Link:** https://arxiv.org/abs/2406.18665
- **Summary:** Learns a lightweight router from human preference data (ChatBot Arena) that predicts whether a query needs the strong or weak model. 2x+ cost reduction while maintaining quality on major benchmarks. Demonstrates transfer: routers trained on one model pair generalize to others at test time. The modern successor to FrugalGPT's cascade idea.
- **Striking finding:** "Our router models also demonstrate significant transfer learning capabilities, maintaining their performance even when the strong and weak models are changed at test time" (Abstract). >2x cost reduction.
- **Implication for curriculum:** Teach routing as a production pattern distinct from cascading - learned classifier vs. confidence threshold.

### Fast Inference from Transformers via Speculative Decoding
- **Authors / Year:** Leviathan, Kalman, Matias (Google) - 2022/2023
- **Venue:** ICML 2023 Oral
- **Link:** https://arxiv.org/abs/2211.17192
- **Summary:** A small draft model proposes K tokens; the large model verifies them in parallel. Output distribution is provably unchanged. 2-3x speedup on T5-XXL without quality loss. The primitive under every fast inference engine today. For harnesses: speculative decoding is why long agent loops are practical at all.
- **Striking finding:** "Inference from large autoregressive models like Transformers is slow - decoding K tokens takes K serial runs of the model" (Sec. 1). 2-3x speedup with identical outputs.
- **Implication for curriculum:** One diagram chapter on "why the agent loop even works at production latency" - speculative decoding is the answer.

### Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
- **Authors / Year:** Snell, Lee, Xu, Kumar (Berkeley/Google DeepMind) - 2024
- **Venue:** arXiv preprint, widely cited
- **Link:** https://arxiv.org/abs/2408.03314
- **Summary:** Shows that compute-optimal test-time allocation (difficulty-aware, prompt-specific) outperforms best-of-N by 4x, and can beat a 14x-larger model on tasks where the smaller model has reasonable baselines. This is the theoretical underpinning for "thinking harder" modes (o1, Claude thinking) and for harness-level effort budgets.
- **Striking finding:** "Enabling LLMs to improve their outputs by using more test-time computation is a critical step towards building generally self-improving agents" (Sec. 1). 4x efficiency gain from adaptive allocation; >14x model-size equivalence in some regimes.
- **Implication for curriculum:** Frame test-time compute as a first-class design variable, alongside model choice and context length.

### The Shift from Models to Compound AI Systems (Berkeley BAIR Blog)
- **Authors / Year:** Zaharia et al. (Berkeley) - 2024
- **Venue:** BAIR Blog (not peer-reviewed, but influential)
- **Link:** https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/
- **Summary:** A manifesto rather than a paper, but it defines the vocabulary the field now uses. A "compound AI system" is a system that uses multiple model calls, retrievers, and tools to solve a task. Reports that 60% of enterprise LLM apps use RAG, 30% use multi-step chains. Argues that compound systems are where quality gains now come from, and that optimization moves from model parameters to system architecture.
- **Striking finding:** "State-of-the-art AI results are increasingly obtained by compound systems with multiple components, not just monolithic models" (para. 2). Databricks survey: 60% RAG, 30% multi-step chains.
- **Implication for curriculum:** Use as the framing essay for the whole book - the student is learning to engineer compound systems, not to prompt-hack one model.

---

## Synthesis: What Should Reshape a Developer Curriculum (≤300 words)

Six findings deserve to restructure the course, not merely appear in it.

**1. The harness, not the model, is where most headroom lives.** SWE-agent's jump from ~4% to 12.5% on SWE-bench came from an Agent-Computer Interface, not a better model (Yang et al. 2024). Open with this. The curriculum's spine is ACI engineering.

**2. Compound systems are the unit of analysis.** Zaharia's BAIR essay reframes the whole field: students are learning to design systems with multiple calls, retrievers, tools - not to prompt a single model. Every chapter should name which compound pattern it exemplifies (cascade, debate, tree, SOP).

**3. Cost-accuracy must be a dual axis from day one.** "AI Agents That Matter" (Kapoor et al. 2024) shows that accuracy-only benchmarks produce needlessly expensive agents. The curriculum should require every student project to plot a Pareto frontier. FrugalGPT's cascade and RouteLLM's learned router are the two reference patterns.

**4. LLM judges are relative, not absolute.** Zheng et al. (MT-Bench) and Thakur et al. (Judging the Judges) agree: position/verbosity/self-enhancement biases mean absolute judge scores are noise. Teach pairwise-with-swap as the default eval protocol, and treat any absolute-score leaderboard with suspicion.

**5. Test-time compute is a design variable.** Snell et al. prove that adaptive test-time compute can beat a 14x-larger model. Frame "thinking harder" as a tunable lever alongside model choice, not a property of specific models.

**6. Security is architectural, not prompt-level.** Agent-SafetyBench shows no major agent scores above 60% safety; StruQ and the Instruction Hierarchy show that channel separation and privilege ordering are the real defenses. Teach sandboxing (ToolEmu) and trust zones (Instruction Hierarchy) as the security chapter's backbone, not "write a better system prompt."

The throughline: treat the harness as a *system* whose cost, safety, and quality are engineered trade-offs - not as a clever prompt.
