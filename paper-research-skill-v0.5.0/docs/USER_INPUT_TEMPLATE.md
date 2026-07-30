# 启动输入模板

用户可以只提供现有信息，缺失项由 Agent 建立待办，不得猜测。

```yaml
target:
  venue_name:
  venue_type: journal | conference | special_issue
  official_urls: []
  call_for_papers_files: []
  deadline:
  deadline_timezone:
  manuscript_language: zh-CN | en | bilingual

researcher:
  broad_fields: [education, communication]
  interests: []
  methods_can_do: []
  methods_avoid: []
  available_software: []
  existing_data: []
  ethics_approval_status:
  zotero_mode: connector | import | web_api | none
  zotero_library_type: personal | group | none

constraints:
  budget:
  weekly_hours:
  desired_submission_date:
  participant_access:
  database_access:
  coding_level:
  must_avoid: []

preferences:
  empirical_or_conceptual:
  quantitative_qualitative_mixed:
  domestic_or_international_focus:
  preferred_output_format: markdown | docx | latex
  source_of_truth: quarto | markdown | word
  citation_style:
  bilingual_abstract_required:
```
