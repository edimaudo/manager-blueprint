"""Original Manager Blueprint capability, scenario, and source-link catalogue.

Publisher resources are linked to their original pages. No full article text is
copied or ingested into the AI knowledge corpus.
"""
from __future__ import annotations

CAPABILITIES = {
    "prioritization": {
        "title": "Prioritization", "domain": "yourself", "domain_label": "Managing Yourself",
        "summary": "Choose the work that matters most, make trade-offs explicit, and protect time for management responsibilities.",
        "why": "Managers inherit work from several directions. Prioritization makes the trade-offs visible so urgent activity does not displace important outcomes.",
        "learn": ["Start with outcomes rather than a task list. Identify the result that matters and the people who depend on it.", "Separate genuinely urgent work from work that is important but can be planned.", "Name what will be deferred, delegated, simplified, or stopped when capacity is constrained.", "Review priorities with the people affected and revisit them when new information changes the trade-offs."],
        "apply": "Use the prioritization planner to compare outcomes, commitments, effort, and strategic alignment. Agree what will be deferred and communicate the decision.",
        "tool": "prioritization-matrix", "scenario": "priority_conflict", "assess": ["I can explain the outcomes that matter most this period.", "I make trade-offs explicit when new work arrives.", "I protect time for work that requires my management attention."],
        "resource_ids": ["ticktick-productivity", "ticktick-calendar", "asana-project-planning", "monday-okrs"]
    },
    "time_management": {
        "title": "Time management", "domain": "yourself", "domain_label": "Managing Yourself",
        "summary": "Design a working rhythm that creates space for focused work, team support, and decisions.",
        "why": "A manager's calendar signals what receives attention. Intentional scheduling reduces reactive work and makes time for people leadership.",
        "learn": ["Review where your time goes before changing your calendar.", "Protect recurring time for one-to-ones, preparation, focused work, and review.", "Group similar administrative tasks and reduce unnecessary context switching.", "Use a weekly review to adjust commitments and identify capacity risks."],
        "apply": "Create a weekly time plan. Identify protected blocks, recurring management commitments, and one activity to reduce or delegate.",
        "tool": "prioritization-matrix", "scenario": "calendar_overload", "assess": ["My calendar reflects my most important responsibilities.", "I leave enough preparation time for important conversations.", "I review my commitments before accepting additional work."],
        "resource_ids": ["ticktick-productivity", "ticktick-calendar", "ticktick-help"]
    },
    "decision_making": {
        "title": "Decision-making", "domain": "yourself", "domain_label": "Managing Yourself",
        "summary": "Make sound decisions with proportionate evidence, clear ownership, and timely communication.",
        "why": "Managers often decide with incomplete information. A practical decision process helps balance speed, risk, and inclusion.",
        "learn": ["Define the decision and the person accountable for making it.", "Distinguish facts, assumptions, constraints, and unknowns.", "Set a timebox and determine how much evidence the decision warrants.", "Communicate the rationale, trade-offs, owner, and review point."],
        "apply": "Write a short decision brief: decision required, options, evidence, risks, consulted stakeholders, decision owner, and date to review.",
        "tool": "prioritization-matrix", "scenario": "decision_under_uncertainty", "assess": ["I make clear who owns a decision.", "I distinguish evidence from assumptions.", "I communicate trade-offs and revisit decisions when conditions change."],
        "resource_ids": ["monday-collaboration", "asana-strategic-planning"]
    },
    "communication": {
        "title": "Manager communication", "domain": "yourself", "domain_label": "Managing Yourself",
        "summary": "Make expectations, updates, and decisions clear for the people who need to act on them.",
        "why": "Clear communication reduces avoidable ambiguity and helps people understand context, ownership, and next steps.",
        "learn": ["Start with the audience and the action or understanding needed.", "Separate the headline from supporting detail.", "Make expectations, owners, dates, and decision points explicit.", "Check understanding and choose an appropriate channel for the message."],
        "apply": "Draft a concise update that states the purpose, context, key message, action required, owner, and timing.",
        "tool": "stakeholder-map", "scenario": "communication_misalignment", "assess": ["I make expectations and responsibilities explicit.", "I adapt detail and language to the audience.", "I confirm understanding when the message has important consequences."],
        "resource_ids": ["monday-collaboration", "asana-strategic-planning"]
    },
    "personal_effectiveness": {
        "title": "Personal effectiveness", "domain": "yourself", "domain_label": "Managing Yourself",
        "summary": "Build reliable habits for reflection, preparation, follow-through, and sustainable performance.",
        "why": "Managers set a working example through how they organize, communicate, respond to pressure, and follow through.",
        "learn": ["Identify recurring situations where your habits help or hinder your effectiveness.", "Use a short preparation routine before important meetings and decisions.", "Close loops by recording commitments, owners, and dates.", "Review what is working and adjust routines rather than relying on willpower alone."],
        "apply": "Choose one management habit to practise for two weeks. Define the trigger, action, and evidence that will show the habit is helping.",
        "tool": "prioritization-matrix", "scenario": "personal_habit_reset", "assess": ["I follow through on commitments or renegotiate them early.", "I prepare for important management interactions.", "I regularly reflect on how my own habits affect the team."],
        "resource_ids": ["ticktick-productivity", "ticktick-help"]
    },
    "one_to_ones": {
        "title": "Effective 1:1 meetings", "domain": "others", "domain_label": "Managing Others",
        "summary": "Use regular one-to-ones to understand progress, remove barriers, coach, and build trust.",
        "why": "A consistent one-to-one rhythm creates a private space for employee priorities, feedback, support, and development.",
        "learn": ["Ask the employee to shape the agenda rather than treating the meeting as a status report.", "Discuss priorities, progress, blockers, decisions, and the support needed.", "Make space for development and feedback, not only immediate delivery.", "Close with a small number of clear commitments, owners, and follow-up dates."],
        "apply": "Use the 1:1 agenda template. Ask the employee what would make the conversation useful and agree on actions before ending.",
        "tool": "one-to-one-agenda", "scenario": "one_to_one_disengagement", "assess": ["My one-to-ones are regular and prepared.", "Employees have meaningful input into the agenda.", "We leave with clear actions and follow-up."],
        "resource_ids": ["monday-collaboration", "asana-team-growth"]
    },
    "delegation": {
        "title": "Delegation", "domain": "others", "domain_label": "Managing Others",
        "summary": "Delegate outcomes with clear context, appropriate authority, support, and checkpoints.",
        "why": "Delegation develops capability and creates capacity. It fails when responsibility is handed over without context, authority, or support.",
        "learn": ["Explain why the outcome matters and how it connects to team priorities.", "Agree the result, boundaries, decision rights, resources, and constraints.", "Match the level of direction and check-in to the person's experience and the risk.", "Review the result and learning without taking ownership back prematurely."],
        "apply": "Complete the delegation planner and discuss the outcome, decision authority, success measures, support, and checkpoints with the employee.",
        "tool": "delegation-planner", "scenario": "delegation_missed_deadline", "assess": ["I delegate outcomes rather than only tasks.", "I clarify decision rights and constraints.", "My check-ins provide support without taking over."],
        "resource_ids": ["asana-project-planning", "monday-collaboration"]
    },
    "employee_coaching": {
        "title": "Coaching employees", "domain": "others", "domain_label": "Managing Others",
        "summary": "Help employees think through challenges, build judgement, and own their next actions.",
        "why": "Effective coaching develops capability instead of making the manager the default problem-solver.",
        "learn": ["Clarify what the employee wants to achieve or resolve.", "Ask open questions before offering a solution.", "Explore options, consequences, and what support is needed.", "Agree an employee-owned action and revisit the learning."],
        "apply": "Use the employee coaching planner to prepare questions, identify support, and agree the employee's next commitment.",
        "tool": "coaching-planner", "scenario": "employee_wants_solution", "assess": ["I ask questions before prescribing solutions.", "I help employees compare options and consequences.", "Employees leave coaching conversations with their own next actions."],
        "resource_ids": ["asana-team-growth", "monday-high-performing-teams"]
    },
    "feedback": {
        "title": "Giving feedback", "domain": "others", "domain_label": "Managing Others",
        "summary": "Deliver timely, specific feedback that explains impact and creates a path forward.",
        "why": "Feedback is more useful when it addresses observable behaviour and its impact rather than making assumptions about intent or personality.",
        "learn": ["Describe the situation and observable behaviour without labels.", "Explain the impact on work, colleagues, customers, or outcomes.", "Invite the other person's perspective and listen for missing context.", "Agree a practical next step and follow-up."],
        "apply": "Prepare the situation, behaviour, impact, question, and next step in the feedback planner.",
        "tool": "feedback-planner", "scenario": "feedback_missed_commitments", "assess": ["I give feedback close to the relevant event.", "I describe observable behaviour and impact.", "I invite the employee's perspective and agree a next step."],
        "resource_ids": ["monday-high-performing-teams", "asana-team-growth"]
    },
    "conflict_management": {
        "title": "Managing conflict", "domain": "others", "domain_label": "Managing Others",
        "summary": "Address disagreement early, understand competing perspectives, and agree workable next steps.",
        "why": "Unaddressed tension can impair decisions, collaboration, and trust. Managers need to surface the issue without turning disagreement into blame.",
        "learn": ["Separate the underlying issue from assumptions about motives.", "Hear each perspective and identify shared outcomes and real points of disagreement.", "Set respectful discussion norms and focus on evidence and impact.", "Agree a decision, experiment, or escalation path with a review point."],
        "apply": "Prepare the issue, parties, perspectives, shared outcome, decision needed, and follow-up before facilitating a conversation.",
        "tool": "feedback-planner", "scenario": "team_conflict", "assess": ["I address tension before it becomes entrenched.", "I understand different perspectives before deciding.", "I help the team agree clear next steps after disagreement."],
        "resource_ids": ["monday-conflict", "monday-collaboration", "asana-team-growth"]
    },
    "performance_management": {
        "title": "Performance conversations", "domain": "others", "domain_label": "Managing Others",
        "summary": "Set clear expectations, discuss evidence fairly, and agree support and accountability.",
        "why": "Performance conversations are most effective when expectations and evidence are clear and the employee can respond.",
        "learn": ["Confirm the expected outcome and the standard that applies.", "Use specific examples and distinguish a pattern from a single incident.", "Ask for the employee's perspective and identify contributing factors.", "Agree actions, support, measures, and a realistic review date."],
        "apply": "Use the performance conversation planner to structure expectations, evidence, employee perspective, support, and review measures.",
        "tool": "performance-conversation", "scenario": "performance_gap", "assess": ["I clarify expectations before evaluating performance.", "I use specific evidence rather than broad labels.", "I agree support, actions, and review dates."],
        "resource_ids": ["monday-high-performing-teams", "asana-team-growth"]
    },
    "employee_development": {
        "title": "Employee development", "domain": "others", "domain_label": "Managing Others",
        "summary": "Understand employee aspirations and build development opportunities into everyday work.",
        "why": "Development is more sustainable when it is connected to real responsibilities, regular feedback, and opportunities to practise.",
        "learn": ["Discuss strengths, interests, career direction, and skills the employee wants to build.", "Identify stretch opportunities that are useful to the team and realistic for the employee.", "Agree support, coaching, and measures of progress.", "Review learning and adjust the development plan as experience grows."],
        "apply": "Create a development conversation plan with one target capability, a practical assignment, support, and a review date.",
        "tool": "coaching-planner", "scenario": "employee_development", "assess": ["I understand what employees want to learn and achieve.", "I create practical opportunities to build capability.", "I follow up on development commitments."],
        "resource_ids": ["asana-team-growth", "monday-high-performing-teams"]
    },
    "manager_alignment": {
        "title": "Working with your manager", "domain": "up", "domain_label": "Managing Up",
        "summary": "Create alignment with your manager on outcomes, priorities, decision rights, and risks.",
        "why": "Clear alignment reduces surprises and helps managers make decisions at the right level.",
        "learn": ["Understand your manager's objectives, constraints, and expectations.", "Clarify outcomes, priorities, decision rights, and escalation triggers.", "Communicate progress and risks early, with options or a recommendation.", "Confirm decisions and commitments in a concise written follow-up."],
        "apply": "Prepare a short alignment brief covering outcomes, current status, risks, decisions needed, and recommended next steps.",
        "tool": "stakeholder-map", "scenario": "conflicting_manager_priorities", "assess": ["I clarify expectations and priorities with my manager.", "I raise risks early with options and recommendations.", "I confirm important decisions and commitments."],
        "resource_ids": ["asana-strategic-planning", "monday-okrs"]
    },
    "stakeholder_management": {
        "title": "Stakeholder management", "domain": "up", "domain_label": "Managing Up",
        "summary": "Understand stakeholder interests, align expectations, and maintain momentum across groups.",
        "why": "Many management outcomes depend on people outside a direct reporting line. Stakeholder work requires clarity, listening, and follow-through.",
        "learn": ["Identify who influences, decides, contributes, or is affected.", "Understand each stakeholder's objectives, concerns, and information needs.", "Adapt the message while keeping the underlying outcome consistent.", "Agree engagement, decision points, and how changes will be communicated."],
        "apply": "Use the stakeholder map to document interests, influence, likely concerns, engagement approach, and next contact.",
        "tool": "stakeholder-map", "scenario": "stakeholder_resistance", "assess": ["I identify the stakeholders who influence important outcomes.", "I understand their interests and concerns.", "I maintain alignment through timely communication and follow-up."],
        "resource_ids": ["asana-strategic-planning", "monday-collaboration", "monday-okrs"]
    },
    "executive_communication": {
        "title": "Executive communication", "domain": "up", "domain_label": "Managing Up",
        "summary": "Communicate decisions, risks, and recommendations in a concise, audience-aware way.",
        "why": "Senior stakeholders need to understand the issue, its implications, and what is required from them.",
        "learn": ["Lead with the decision, outcome, or issue that matters.", "Use only the evidence needed to explain the implications.", "State the options, trade-offs, recommendation, and decision required.", "Be explicit about timing, ownership, and risks."],
        "apply": "Prepare a one-page executive update: headline, status, evidence, risk, recommendation, decision required, and owner.",
        "tool": "stakeholder-map", "scenario": "executive_risk_update", "assess": ["I tailor the level of detail to the audience.", "I lead with the outcome or decision required.", "I communicate risks and recommendations clearly."],
        "resource_ids": ["asana-strategic-planning", "monday-okrs"]
    },
    "influence": {
        "title": "Influence without authority", "domain": "up", "domain_label": "Managing Up",
        "summary": "Build commitment by understanding other priorities and connecting proposals to shared outcomes.",
        "why": "Managers often need cooperation across teams without formal authority. Influence grows through credibility, clarity, and reciprocal problem-solving.",
        "learn": ["Understand what matters to the people you need to influence.", "Frame the proposal around shared outcomes and practical benefits.", "Invite concerns early and adapt the path without losing the objective.", "Make commitments specific and close the loop."],
        "apply": "Prepare a stakeholder conversation with the shared goal, likely objections, evidence, possible trade-offs, and a specific ask.",
        "tool": "stakeholder-map", "scenario": "influence_cross_functional", "assess": ["I understand what matters to the people I need to influence.", "I connect proposals to shared goals.", "I seek commitment through dialogue and follow-through."],
        "resource_ids": ["monday-collaboration", "asana-strategic-planning"]
    },
    "skip_level_meetings": {
        "title": "Skip-level meetings", "domain": "up", "domain_label": "Managing Up",
        "summary": "Use skip-level conversations to learn, share themes responsibly, and strengthen alignment.",
        "why": "Skip-level meetings can provide broader context, but they require care around transparency, confidentiality, and reporting-line trust.",
        "learn": ["Clarify the purpose and expected outcome of the meeting.", "Ask open questions about priorities, barriers, and organizational context.", "Share themes and evidence without exposing confidential individual details.", "Close with agreed follow-up and keep your manager appropriately informed."],
        "apply": "Use the skip-level planner to organize purpose, insights, questions, risks, and follow-up commitments.",
        "tool": "skip-level-planner", "scenario": "skip_level_concern", "assess": ["I prepare a clear purpose for skip-level meetings.", "I share themes responsibly and protect confidential information.", "I close the loop with appropriate stakeholders."],
        "resource_ids": ["asana-strategic-planning", "monday-collaboration"]
    },
    "visibility": {
        "title": "Visibility and career growth", "domain": "up", "domain_label": "Managing Up",
        "summary": "Make outcomes, learning, and development goals visible without relying on self-promotion alone.",
        "why": "Visibility helps decision-makers understand impact, emerging risks, and where support or opportunity may be needed.",
        "learn": ["Connect updates to measurable outcomes and organizational priorities.", "Share progress and risks consistently rather than only at milestone points.", "Ask for specific feedback and clarify development expectations.", "Build relationships across relevant teams and contribute to shared outcomes."],
        "apply": "Draft a concise impact update showing outcomes, lessons, risks, and the support or opportunity you are seeking.",
        "tool": "stakeholder-map", "scenario": "visibility_update", "assess": ["I communicate outcomes and progress clearly.", "I ask for feedback about expectations and development.", "I build relationships beyond my immediate team."],
        "resource_ids": ["asana-strategic-planning", "monday-okrs"]
    },
}

SCENARIOS = {
    "priority_conflict": {"title":"Two urgent priorities compete", "capability":"prioritization", "role":"Your manager", "brief":"You have two urgent requests from different stakeholders and not enough capacity to deliver both by the same deadline. You need to clarify outcomes, negotiate trade-offs, and recommend a priority."},
    "calendar_overload": {"title":"Your calendar is overloaded", "capability":"time_management", "role":"A peer manager", "brief":"A peer asks you to take on another recurring meeting and several operational tasks. Your calendar is already crowded and your team needs more access to you."},
    "personal_habit_reset": {"title":"Your management habits are slipping", "capability":"personal_effectiveness", "role":"Your manager", "brief":"Several important follow-ups have slipped because your days are reactive. Your manager asks how you will rebuild a reliable routine while staying available to the team."},
    "decision_under_uncertainty": {"title":"A decision with incomplete information", "capability":"decision_making", "role":"A senior stakeholder", "brief":"A decision is due soon but some data is incomplete. You need to explain what is known, what remains uncertain, the risks, and the decision path."},
    "communication_misalignment": {"title":"A project update was misunderstood", "capability":"communication", "role":"A cross-functional stakeholder", "brief":"A written update led two teams to make different assumptions about an owner and a deadline. Clarify the message, acknowledge the ambiguity, and agree the action, owner, and timing."},
    "one_to_one_disengagement": {"title":"An employee seems disengaged", "capability":"one_to_ones", "role":"An employee", "brief":"You are in a one-to-one with an employee who gives short answers and says everything is fine, but their engagement and delivery have changed."},
    "delegation_missed_deadline": {"title":"A delegated assignment is late", "capability":"delegation", "role":"An employee", "brief":"An employee you delegated work to has missed an important checkpoint. They say they were unsure what decisions they could make and did not want to interrupt you."},
    "employee_wants_solution": {"title":"An employee wants you to solve the problem", "capability":"employee_coaching", "role":"An employee", "brief":"An employee brings you a recurring problem and asks you to tell them exactly what to do. Your aim is to coach them toward their own options and next action."},
    "feedback_missed_commitments": {"title":"Repeated missed commitments", "capability":"feedback", "role":"An employee", "brief":"An employee has missed several agreed deadlines. They are capable and well-intentioned but become defensive when challenged. You need to give clear, fair feedback."},
    "team_conflict": {"title":"Two team members disagree", "capability":"conflict_management", "role":"A team member", "brief":"Two experienced team members disagree strongly about how work should be delivered. The disagreement is slowing the team and affecting collaboration."},
    "performance_gap": {"title":"A sustained performance gap", "capability":"performance_management", "role":"An employee", "brief":"An employee's work has not consistently met agreed standards despite prior informal conversations. You need to discuss evidence, impact, support, and accountability."},
    "conflicting_manager_priorities": {"title":"Your manager gives conflicting priorities", "capability":"manager_alignment", "role":"Your manager", "brief":"Your manager gives you two priorities that cannot both be completed with the available capacity. You need to clarify the intended trade-off and agree what changes."},
    "stakeholder_resistance": {"title":"A stakeholder resists your proposal", "capability":"stakeholder_management", "role":"A peer stakeholder", "brief":"A peer stakeholder resists a change you are proposing because they see risk and extra work for their team. Explore their concerns and seek a workable agreement."},
    "influence_cross_functional": {"title":"You need support without authority", "capability":"influence", "role":"A skeptical peer leader", "brief":"A cross-functional change needs support from a peer leader who does not report to you. They are concerned about workload and competing priorities. Understand their interests and build a workable commitment."},
    "executive_risk_update": {"title":"Communicate a delivery risk upward", "capability":"executive_communication", "role":"An executive", "brief":"A key deliverable is at risk. You need to give a concise update with impact, evidence, options, a recommendation, and a decision required."},
    "skip_level_concern": {"title":"A sensitive issue in a skip-level", "capability":"skip_level_meetings", "role":"A senior leader", "brief":"In a skip-level conversation, a leader asks how the team is doing. You need to raise a recurring issue without exposing confidential employee details or undermining your manager."},
    "visibility_update": {"title":"Explain your team's impact", "capability":"visibility", "role":"A senior stakeholder", "brief":"A senior stakeholder asks what your team has delivered and what matters next. You need to communicate outcomes, lessons, and a clear request without overstating impact."},
    "employee_development": {"title":"Discuss an employee's development", "capability":"employee_development", "role":"An employee", "brief":"An employee wants to grow but is unsure what skills to build or how to get experience. Help them identify a practical development opportunity and support."},
}

RESOURCES = [
    {"id":"monday-collaboration", "title":"Project collaboration: tips to improve team performance", "source":"monday.com", "url":"https://monday.com/blog/project-management/project-collaboration/", "summary":"A starting point for building shared clarity, defining ownership, improving communication, and making progress visible across a team.", "domain":"others", "capabilities":["one_to_ones","delegation","stakeholder_management","influence","skip_level_meetings"], "kind":"Article"},
    {"id":"monday-conflict", "title":"Workplace conflict management: strategies to boost teamwork", "source":"monday.com", "url":"https://monday.com/blog/project-management/conflict-management/", "summary":"A practical reference for recognizing and addressing disagreement so that team friction can be handled constructively.", "domain":"others", "capabilities":["conflict_management","feedback"], "kind":"Article"},
    {"id":"monday-high-performing-teams", "title":"High-performing teams", "source":"monday.com", "url":"https://monday.com/blog/teamwork/high-performing-teams/", "summary":"A team-effectiveness starting point covering collaboration, communication, creativity, and consistent delivery.", "domain":"others", "capabilities":["employee_coaching","feedback","performance_management","employee_development"], "kind":"Article"},
    {"id":"monday-okrs", "title":"OKRs for project management: examples and how-to guide", "source":"monday.com", "url":"https://monday.com/blog/project-management/okr-for-project-management/", "summary":"A reference for connecting objectives to measurable results and keeping execution aligned with intended outcomes.", "domain":"up", "capabilities":["prioritization","manager_alignment","stakeholder_management","executive_communication","visibility"], "kind":"Article"},
    {"id":"asana-team-growth", "title":"Team growth and focus resources", "source":"Asana", "url":"https://asana.com/resources/category/team-growth", "summary":"A resource collection for managers and leaders focused on personal productivity and team output. Use it as a starting point for team effectiveness and development topics.", "domain":"others", "capabilities":["one_to_ones","employee_coaching","feedback","conflict_management","performance_management","employee_development"], "kind":"Collection"},
    {"id":"asana-strategic-planning", "title":"Strategic planning resources", "source":"Asana", "url":"https://asana.com/resources/category/strategic-planning", "summary":"A collection for translating strategy into aligned plans, priorities, and coordinated work across teams.", "domain":"up", "capabilities":["decision_making","manager_alignment","stakeholder_management","executive_communication","influence","skip_level_meetings","visibility"], "kind":"Collection"},
    {"id":"asana-project-planning", "title":"Project planning resources", "source":"Asana", "url":"https://asana.com/resources/category/project-planning", "summary":"A collection of planning and tracking resources that can support delegation, work ownership, and delivery coordination.", "domain":"yourself", "capabilities":["prioritization","time_management","delegation","decision_making"], "kind":"Collection"},
    {"id":"ticktick-productivity", "title":"How to stay productive every day with a simple TickTick system", "source":"TickTick", "url":"https://ticktick.com/resources/article/7491396495875244032/stay-productive-every-day-with-ticktick", "summary":"A productivity reference to explore personal task organization and repeatable routines. The application should adapt the ideas to a manager's responsibilities rather than simply reproduce a personal to-do system.", "domain":"yourself", "capabilities":["prioritization","time_management","personal_effectiveness"], "kind":"Article"},
    {"id":"ticktick-calendar", "title":"How I use TickTick's calendar to stay organized", "source":"TickTick", "url":"https://ticktick.com/resources/article/7340680464711024640/calendar-workflows-guide", "summary":"A calendar-workflow example for organizing work over time and connecting tasks with scheduled commitments.", "domain":"yourself", "capabilities":["prioritization","time_management","personal_effectiveness"], "kind":"Article"},
    {"id":"ticktick-help", "title":"TickTick help centre: tasks, calendar, matrix, focus, and habits", "source":"TickTick", "url":"https://help.ticktick.com/", "summary":"Product guidance covering task organization, calendar planning, the Eisenhower Matrix, focus routines, and habit tracking. These ideas can inform personal effectiveness exercises.", "domain":"yourself", "capabilities":["prioritization","time_management","decision_making","personal_effectiveness"], "kind":"Help centre"},
    {"id":"ticktick-productivity-hub", "title":"TickTick Productivity Hub", "source":"TickTick", "url":"https://ticktick.com/resources", "summary":"The publisher's collection of productivity guides, including task organization, calendar use, and routines.", "domain":"yourself", "capabilities":["prioritization","time_management","personal_effectiveness"], "kind":"Collection"},
]

GOAL_TO_CAPABILITY = {
    "Prioritization and time management":"prioritization", "Decision-making":"decision_making",
    "Communication":"communication", "Leadership mindset":"personal_effectiveness",
    "Personal effectiveness":"personal_effectiveness", "Running effective 1:1s":"one_to_ones",
    "Delegation":"delegation", "Coaching employees":"employee_coaching", "Giving feedback":"feedback",
    "Handling conflict":"conflict_management", "Performance conversations":"performance_management",
    "Hiring and employee development":"employee_development", "Working with my manager":"manager_alignment",
    "Stakeholder management":"stakeholder_management", "Executive communication":"executive_communication",
    "Influence":"influence", "Skip-level meetings":"skip_level_meetings", "Visibility and career growth":"visibility"
}

ASSESSMENT_QUESTIONS = [
    ("yourself", "prioritization", "I can identify the most important outcomes and make trade-offs when capacity is limited."),
    ("yourself", "time_management", "I plan my calendar to protect time for important management responsibilities."),
    ("yourself", "decision_making", "I make timely decisions using proportionate evidence and clear ownership."),
    ("yourself", "communication", "I communicate expectations and decisions in a way the audience can act on."),
    ("yourself", "personal_effectiveness", "I follow through on commitments and review how my own habits affect my work."),
    ("others", "one_to_ones", "My one-to-one meetings create useful space for employee priorities, support, and development."),
    ("others", "delegation", "I delegate outcomes with clear context, authority, and appropriate follow-up."),
    ("others", "employee_coaching", "I use questions to help employees think through challenges and own next steps."),
    ("others", "feedback", "I give timely feedback using observable behaviour and its impact."),
    ("others", "conflict_management", "I address disagreement constructively and help people agree workable next steps."),
    ("others", "performance_management", "I clarify expectations and address performance gaps using specific evidence."),
    ("others", "employee_development", "I create practical opportunities for employees to develop their capabilities."),
    ("up", "manager_alignment", "I align priorities, expectations, and decision rights with my manager."),
    ("up", "stakeholder_management", "I understand stakeholder interests and maintain alignment across groups."),
    ("up", "executive_communication", "I communicate risks, decisions, and recommendations concisely to senior audiences."),
    ("up", "influence", "I build commitment with people outside my reporting line."),
    ("up", "skip_level_meetings", "I use skip-level conversations appropriately and follow up on themes responsibly."),
    ("up", "visibility", "I make outcomes, risks, and development goals visible to relevant decision-makers."),
]


def score_management_style(answers: dict[str, str]) -> dict:
    """Create a nuanced original reflection profile, including close/tied patterns."""
    disc_keys = ("d", "i", "s", "c")
    strength_keys = ("ex", "in", "re", "st")
    labels = {"d":"Driver", "i":"Connector", "s":"Stabilizer", "c":"Analyst"}
    domain_labels = {"ex":"Execution", "in":"Influence", "re":"Relationship Building", "st":"Strategic Thinking"}
    disc = {key: sum(answers[str(i)] == key for i in range(1, 7)) for key in disc_keys}
    strengths = {key: sum(answers[str(i)] == key for i in range(7, 13)) for key in strength_keys}
    disc_sorted = sorted(disc, key=lambda k: (-disc[k], disc_keys.index(k)))
    strength_sorted = sorted(strengths, key=lambda k: (-strengths[k], strength_keys.index(k)))
    # Treat a one-answer difference as a supporting tendency; never force a false single-style result.
    top_disc = [key for key in disc_sorted if disc[key] > 0 and disc[key] >= disc[disc_sorted[0]] - 1][:2]
    top_strengths = [key for key in strength_sorted if strengths[key] > 0 and strengths[key] >= strengths[strength_sorted[0]] - 1][:2]
    primary = disc_sorted[0]
    strength = strength_sorted[0]
    archetype = f"{' / '.join(labels[x] for x in top_disc)} · {' / '.join(domain_labels[x] for x in top_strengths)}"
    desc = {
        "d":"You may bring urgency, ownership, and a strong focus on outcomes.",
        "i":"You may build momentum through communication, connection, and enthusiasm.",
        "s":"You may create stability through consistency, support, and dependable relationships.",
        "c":"You may strengthen decisions through evidence, standards, and careful analysis.",
    }
    strength_desc = {
        "ex":"You may bring structure, reliability, and follow-through.",
        "in":"You may build support and communicate ideas persuasively.",
        "re":"You may build trust and help people work together.",
        "st":"You may recognize patterns, consider options, and think ahead.",
    }
    watchouts = {
        "d":"Check whether speed is limiting input or understanding; explain the reasoning behind decisions.",
        "i":"Translate ideas and enthusiasm into clear owners, decisions, and follow-through.",
        "s":"Raise difficult issues early and make expectations explicit, even when conversations are uncomfortable.",
        "c":"Time-box analysis and distinguish essential evidence from detail that will not change the decision.",
    }
    coaching = {
        "d":"Be concise and outcome-oriented. Challenge assumptions, identify trade-offs, and agree measurable next steps.",
        "i":"Use dialogue and examples. Connect actions to people and influence, then make commitments visible.",
        "s":"Build context and trust. Allow reflection time while still making decisions and expectations clear.",
        "c":"Use structured reasoning, explicit evidence, options, and clear decision criteria.",
    }
    approach_by_pair = {
        ("d","ex"):"Use your drive to establish clear outcomes and milestones. Add listening checkpoints so speed does not suppress employee input.",
        ("d","in"):"Use your momentum to build commitment. Make space for concerns and confirm that enthusiasm has turned into shared ownership.",
        ("d","re"):"Combine decisiveness with trust-building. Explain the why, check the impact on people, and remain clear about accountability.",
        ("d","st"):"Connect decisive action to a longer-term direction. State assumptions and revisit the decision when evidence changes.",
        ("i","ex"):"Turn energy and ideas into clear owners, milestones, and follow-through. Make commitments visible after collaborative discussions.",
        ("i","in"):"Use communication and influence to align people around a shared outcome. Avoid assuming agreement just because the discussion is positive.",
        ("i","re"):"Build connection and participation while keeping expectations and difficult feedback explicit.",
        ("i","st"):"Use your ability to connect ideas to create a compelling direction, then translate it into practical decisions and actions.",
        ("s","ex"):"Use consistency to create dependable routines and follow-through. Raise missed commitments early rather than waiting to preserve harmony.",
        ("s","in"):"Build support through steady relationships and thoughtful communication. Be direct about the decision or commitment needed.",
        ("s","re"):"Use trust and empathy to develop people. Pair support with clear standards and timely performance conversations.",
        ("s","st"):"Bring people into longer-term thinking and translate the direction into manageable stages and clear ownership.",
        ("c","ex"):"Use structure and standards to improve reliable delivery. Time-box analysis so the team can act with sufficient evidence.",
        ("c","in"):"Use evidence and careful reasoning to build credibility. Simplify the message so stakeholders can understand and support the recommendation.",
        ("c","re"):"Pair careful analysis with curiosity about people and context. Check how decisions land rather than assuming the facts speak for themselves.",
        ("c","st"):"Use analysis and pattern recognition to anticipate consequences. Communicate a clear recommendation rather than leaving others with options alone."
    }
    management_approach = approach_by_pair.get((primary, strength), coaching[primary])
    return {
        "archetype": archetype,
        "primary_style": primary,
        "supporting_styles": top_disc,
        "strength_pattern": strength,
        "top_strength_domains": top_strengths,
        "disc_scores": disc,
        "strength_domain_scores": strengths,
        "disc_percentages": {k: round(v / 6 * 100) for k, v in disc.items()},
        "strength_domain_percentages": {k: round(v / 6 * 100) for k, v in strengths.items()},
        "profile_summary": "Your result highlights patterns in how you tend to approach people, decisions, and delivery. Close scores are shown as supporting tendencies rather than forcing a single label.",
        "strengths": [desc[x] for x in top_disc] + [strength_desc[x] for x in top_strengths],
        "watchouts": watchouts[primary],
        "coaching_approach": coaching[primary],
        "management_approach": management_approach,
        "potential_weaknesses": [watchouts[primary], "A preferred style can become less effective when applied the same way to every employee or situation."],
        "management_adjustments": [
            "Ask employees how they prefer to receive context and feedback rather than assuming they work like you.",
            "Pair your natural strengths with a deliberate check for the needs your preferred approach may overlook.",
            "Use the profile as a reflection prompt and test which behaviours work in the situation at hand."
        ],
        "disclaimer": "This original developmental reflection draws on publicly described behavioral-style concepts and broad strengths domains. It is not a validated psychometric diagnosis, an official DiSC report, or a CliftonStrengths assessment and does not reproduce their proprietary question banks."
    }


def recommend_capabilities(goals: list[dict], baseline_result: dict | None, progress_rows: list[dict]) -> list[str]:
    """Rank user-selected capabilities using goal priority, baseline and completion."""
    goal_weight = {g.get("capability_slug"): int(g.get("priority", 3)) for g in goals if g.get("capability_slug") in CAPABILITIES}
    scores = (baseline_result or {}).get("capability_scores", {}) if baseline_result else {}
    progress = {}
    for row in progress_rows:
        if row.get("status") == "completed":
            progress.setdefault(row.get("capability_slug"), set()).add(row.get("step"))
    candidates = set(goal_weight) | {k for k in scores if k in CAPABILITIES}
    if not candidates:
        return ["one_to_ones", "delegation", "prioritization"]
    def rank(slug: str):
        baseline = scores.get(slug)
        gap = (5 - float(baseline)) if baseline is not None else 1.5
        unfinished = 4 - len(progress.get(slug, set()))
        selected = goal_weight.get(slug, 0)
        return (selected * 1.5 + gap + unfinished * 0.15, selected, gap, slug)
    return sorted(candidates, key=rank, reverse=True)[:3]
