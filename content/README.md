# Manager Blueprint content folder

Use this folder to collect and organize the management content supplied for Manager Blueprint. Keep the original source files here so they can be reviewed, revised, and added to the product in a controlled way.

## Folder guide

- `inbox/`: newly supplied material that has not yet been reviewed or categorized.
- `knowledge/`: original management guidance, topic explainers, examples, and reference notes.
- `frameworks/`: management frameworks and playbooks that can be used in learning and coaching.
- `tools_and_templates/`: worksheets, checklists, planners, conversation guides, and templates.
- `practice_scenarios/`: realistic management situations for guided practice and role-play.
- `coaching/`: coaching principles, facilitator guidance, and the four coaching interaction styles (Action-oriented, Connector, Reflective, Analytical).
- `assessment_reference/`: assessment design notes, item rationale, scoring documentation, and authorized reference material. Do not add proprietary assessment question banks without the necessary licence.

## How supplied content reaches the application

This folder is a source-material staging area. Files copied here are **not automatically published or indexed** by the running application.

To make approved material available in the current application, an administrator uses **Administration → Publish management documentation → Upload and index**. The application currently accepts PDF, TXT, and Markdown (`.md`) files. The current upload path extracts text, stores the original in private Supabase Storage, creates searchable text chunks, and makes approved excerpts available to contextual AI coaching according to the document's access tier and publication status.

Current upload limits are 20 MB per file, 500 PDF pages, and 2 MB of extracted text. The application does not currently accept DOCX through this admin upload form.

## Before content is published

1. Confirm that the material is owned by you or that you have permission to use it.
2. Remove confidential business information, personal information, and employee records unless there is a documented and approved reason to process them.
3. Record the title, author or source, source URL where applicable, intended management domain/capability, access tier (Free, Manager Plus, or Manager Pro), and review date.
4. Check that the document is readable and that its guidance is appropriate for the intended audience.
5. Upload it through the admin interface and verify that the indexed excerpts are accurate before relying on them in coaching.

External publisher articles should remain links to their original publishers with original summaries. Do not copy full publisher articles into this folder or the AI knowledge base unless you have the necessary rights.

## Suggested file naming

Use a clear, stable name such as:

- `managing-others_feedback-framework_v1.md`
- `managing-yourself_prioritization-guide_2026-11.pdf`
- `managing-up_stakeholder-map-template_v1.pdf`
- `coaching_roleplay_performance-conversation_v1.md`

Keep drafts in `inbox/` until they are reviewed. Move approved source files into the relevant category folder.
