# Manager Blueprint — content and framework sources

## Product design basis

The application follows the supplied Manager Blueprint PRD. The Blueprint is the central experience and organizes development around Managing Yourself, Managing Others, and Managing Up. Each capability uses a Learn / Apply / Practice / Assess flow. Tools, templates, coaching, and resources are embedded in that capability context rather than treated as separate products.

## Publisher resources used as the initial knowledge-library starting point

The app contains a curated list of external publisher resources with original short summaries and links. This is a complimentary resource directory, not a lesson library. It does not scrape, mirror, or ingest full article text. Users open the resources at the publisher's site. The short summaries are Manager Blueprint signposts and do not replace or reproduce the publisher's content.

Keep two concepts separate in the product: capability guidance is concise, first-party guidance embedded in the relevant capability page (why the capability matters, practical principles, and an application prompt); publisher resources are optional links for further reading outside the app. Neither should be turned into a long-form course or LMS lesson unless the product requirements change.

### monday.com

- Project collaboration: tips to improve team performance — https://monday.com/blog/project-management/project-collaboration/ — used as a starting point for shared clarity, clear ownership, communication norms, and progress visibility.
- Workplace conflict management: strategies to boost teamwork — https://monday.com/blog/project-management/conflict-management/ — starting point for constructive handling of team disagreement.
- High-performing teams — https://monday.com/blog/teamwork/high-performing-teams/ — starting point for team effectiveness and collaboration.
- OKRs for project management — https://monday.com/blog/project-management/okr-for-project-management/ — starting point for connecting objectives to measurable outcomes and execution.

### Asana

- Team growth and focus resources — https://asana.com/resources/category/team-growth — collection for manager and leader productivity and team output.
- Strategic planning resources — https://asana.com/resources/category/strategic-planning — collection for strategic alignment and coordinated planning.
- Project planning resources — https://asana.com/resources/category/project-planning — collection for planning and tracking work.

### TickTick

- Productivity Hub — https://ticktick.com/resources — publisher collection of productivity guides.
- How to stay productive every day with a simple TickTick system — https://ticktick.com/resources/article/7491396495875244032/stay-productive-every-day-with-ticktick — starting point for task organization and repeatable routines.
- How I use TickTick's calendar to stay organized — https://ticktick.com/resources/article/7340680464711024640/calendar-workflows-guide — starting point for calendar workflows.
- TickTick Help Center — https://help.ticktick.com/ — product guidance covering task management, calendar planning, the Eisenhower Matrix, focus, and habits.

Resource pages and linked titles were checked on 2026-11-01. Publisher content and URLs can change. The app uses publisher links and original short summaries; it does not automatically synchronize their sites or index the full articles for Gemini. The capability-specific short summaries are passed to Gemini as resource signposts, not as full-text evidence.

## Future organization-specific materials

Documentation from Canadian Tire, Manulife, and Home Depot has not been supplied yet and is not included in the current content catalogue or Gemini retrieval corpus. When provided, each document should be reviewed for ownership, permission to use, confidential or personal information, and intended audience before it is uploaded. The current document uploader can accept authorized material, but company/source metadata and a separate organization-specific collection have not been implemented yet. Those can be added when the documents are supplied and their intended use is known. No company-specific process, policy, model, or internal practice has been invented or preloaded.

## Manager Style Profile

The current Manager Style Profile uses 32 original, management-specific statements across eight dimensions: four behavioural preferences informed by publicly described DiSC concepts and four contribution domains used by Gallup to organize CliftonStrengths themes. The statements are independently authored; no official DiSC or CliftonStrengths question banks are reproduced.

The scoring model averages four five-point responses for each dimension, reverse-scores selected statements, normalizes each dimension to a 0–100 descriptive scale, identifies leading and closely aligned secondary tendencies, and combines the leading behavioural preference with the leading contribution domain into one of 16 original management-style descriptions. Scores are not percentiles, population norms, or official results. The instrument has not been psychometrically validated and must be refined through consented pilot testing before stronger reliability claims are made. It does not identify Gallup's 34 individual themes or issue an official DiSC profile.

### Management-style background references

- Everything DiSC — https://www.everythingdisc.com/what-is-disc
- Gallup's four CliftonStrengths domains — https://www.gallup.com/cliftonstrengths/en/253736/cliftonstrengths-domains.aspx
- Gallup's 34 CliftonStrengths themes — https://www.gallup.com/cliftonstrengths/en/253715/home.aspx
- Gallup assessment structure — https://support.gallup.com/hc/en-us/articles/4415092592275-How-is-the-CliftonStrengths-assessment-structured

These sources are conceptual references only. The application does not call these sites, retrieve their assessments, use their proprietary questions, or claim to produce official assessment results.

## Coaching foundation

The coaching instructions are informed by the broad management practices identified in the PRD and by the user's stated interest in *The Effective Manager*. The app does not reproduce the book's text. The AI coach can use administrator-uploaded, authorized documents as supporting context. External publisher links are passed as short curated signposts when relevant, not as full-text sources.

## External source handling

- External resource summaries are written in original language and point to the publisher's page.
- Full publisher articles are not copied into the app or the Gemini retrieval corpus.
- Admin-uploaded PDFs and text documents remain a separate private knowledge source, subject to the document's access tier and storage rules.
- Do not upload copyrighted or confidential documents without permission.


## Billing

No external payment processor is active. The implementation currently retains a provider-neutral catalogue and entitlement schema with disabled placeholder checkout and billing-management endpoints.
