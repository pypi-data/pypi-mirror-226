NEGATIVE_MULTILINE_STRING_START = "(?!>>>\n)"
NEGATIVE_MULTILINE_STRING_END = "(?!^<<<)"

STRICTDOC_BASIC_TYPE_SYSTEM = rf"""
FieldName[noskipws]:
  /[A-Z]+[A-Z_]*/
;

// According to the Strict Grammar Rule #3, both SingleLineString and
// MultiLineString can never be empty strings.
// Both must eventualy start with a non-space character.
SingleLineString:
  /{NEGATIVE_MULTILINE_STRING_START}\S.*$/
;


MultiLineString[noskipws]:
  />>>\n/-
  /(?ms){NEGATIVE_MULTILINE_STRING_END} *{NEGATIVE_MULTILINE_STRING_END}\S({NEGATIVE_MULTILINE_STRING_END}.)+/
  /^<<</-
;

Reference[noskipws]:
  // FileReference is an early, experimental feature. Do not use yet.
  ParentReqReference | ChildReqReference | FileReference | BibReference
;

ParentReqReference[noskipws]:
  '- TYPE: Parent' '\n'
  '  VALUE: ' ref_uid = /.*$/ '\n'
;

ChildReqReference[noskipws]:
  '- TYPE: Child' '\n'
  '  VALUE: ' ref_uid = /.*$/ '\n'
;


FileReference[noskipws]:
  // FileReference is an early, experimental feature. Do not use yet.
  '- TYPE: File' '\n'
  g_file_entry = FileEntry
;

FileEntry[noskipws]:
  ('  FORMAT: ' g_file_format = FileEntryFormat '\n')?
   '  VALUE: ' g_file_path = /.*$/ '\n'
;

FileEntryFormat[noskipws]:
  'Sourcecode' | 'Python' | /[A-Z]+[A-Z_]*/
;

BibReference[noskipws]:
  '- TYPE: BibRef' '\n'
  bib_entry = BibEntry
;

BibEntry[noskipws]:
  ('  FORMAT: ' bib_format = BibEntryFormat '\n')?
   '  VALUE: ' bib_value = /.*$/ '\n'
;

BibEntryFormat[noskipws]:
  'String' | 'BibTex' | 'Citation'
;

"""
