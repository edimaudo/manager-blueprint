# Content and framework source notes

## Management foundations

- **The Effective Manager: Completely Revised and Updated**, Mark Horstman, Kate Braun, and Sarah Sentes — the coaching prompt is oriented around broad management practices such as regular one-to-ones, feedback, coaching, and delegation. The app does not reproduce the book's text or proprietary materials. Add only excerpts/documents the administrator has permission to use.

## Management-style reflection

- **DISC / DiSC:** https://www.discprofile.com/disc-styles — public description of Dominance, Influence, Steadiness, and Conscientiousness. The app uses original reflection questions and does not reproduce official DiSC question banks or claim to issue an official DiSC profile.
- **CliftonStrengths:** https://www.gallup.com/cliftonstrengths/en/home.aspx and https://www.gallup.com/cliftonstrengths/en/253736/cliftonstrengths-domains.aspx — the app's second question set is an original reflection across broad work-contribution domains (execution, influence, relationship building, and strategic thinking). It is not the CliftonStrengths assessment and does not produce Gallup results.
- **Combining strengths and DiSC:** https://boarcommunity.com/combining-clifton-strengthsfinder-and-wiley-everything-disc-workplace/ — supplied as additional background for considering both behavior preferences and strengths-based contribution patterns.

## Article and coach-archetype sources

- TickTick resources: https://ticktick.com/resources
- Asana resources: https://asana.com/resources
- monday.com blog: https://monday.com/blog
- Strawberry.me archetypes: https://strawberry.me/resources/archetypes

The app provides curated publisher links and lets administrators add approved article URLs. It does not scrape or republish complete articles from these publishers. The Strawberry.me page could not be verified during this build, so the five-question coach quiz uses original interaction preferences and includes a link to the supplied reference rather than claiming to reproduce its archetypes.

## LLM grounding

Administrator-uploaded PDFs and text documents are stored privately, chunked, and indexed for Postgres full-text retrieval. Retrieved excerpts are passed to Gemini as reference context, subject to each user's resource entitlement. External publisher URLs are not currently ingested into the LLM corpus; administrators should upload material they have permission to use or add publisher links for readers to open at source.
