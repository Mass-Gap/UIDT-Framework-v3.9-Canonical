-- =============================================================================
-- UIDT-OS SQLite Schema v1.0
-- Compatible with Supabase schema, adapted for SQLite
-- =============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- TABLES

CREATE TABLE IF NOT EXISTS studies (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
title TEXT NOT NULL,
description TEXT,
research_question TEXT,
uidt_version TEXT DEFAULT '3.7.2',
primary_claim_id TEXT,
status TEXT DEFAULT 'active',
created_at TEXT DEFAULT (datetime('now')),
updated_at TEXT DEFAULT (datetime('now')),
created_by TEXT,
tags TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS experiments (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
study_id TEXT REFERENCES studies(id) ON DELETE CASCADE,
name TEXT NOT NULL,
hypothesis TEXT,
methodology TEXT,
parameters TEXT DEFAULT '{}',
expected_outcome TEXT,
target_evidence TEXT DEFAULT 'D' CHECK (target_evidence IN ('A', 'A-', 'B', 'C', 'D', 'E')),
status TEXT DEFAULT 'designed',
created_at TEXT DEFAULT (datetime('now')),
updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS runs (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
run_number INTEGER NOT NULL,
status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
started_at TEXT,
completed_at TEXT,
duration_seconds REAL,
config TEXT DEFAULT '{}',
seed INTEGER,
results TEXT DEFAULT '{}',
residual REAL,
stdout TEXT,
stderr TEXT,
script_hash TEXT,
environment TEXT DEFAULT '{}',
created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS artifacts (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
study_id TEXT REFERENCES studies(id) ON DELETE SET NULL,
run_id TEXT REFERENCES runs(id) ON DELETE SET NULL,
name TEXT NOT NULL,
type TEXT DEFAULT 'other' CHECK (type IN ('pdf', 'latex', 'python', 'json', 'csv', 'data', 'figure', 'other')),
mime_type TEXT,
size_bytes INTEGER,
storage_path TEXT,
storage_location TEXT DEFAULT 'local' CHECK (storage_location IN ('local', 'supabase')),
checksum_sha256 TEXT,
embedding BLOB,
content_preview TEXT,
doi TEXT,
metadata TEXT DEFAULT '{}',
created_at TEXT DEFAULT (datetime('now')),
created_by TEXT
);

CREATE TABLE IF NOT EXISTS prompts (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
name TEXT NOT NULL,
version TEXT NOT NULL,
system_prompt TEXT,
user_template TEXT,
model TEXT DEFAULT 'claude-opus-4-5-20251101',
temperature REAL DEFAULT 0.0,
max_tokens INTEGER,
content_hash TEXT,
purpose TEXT,
expected_output_format TEXT,
is_active INTEGER DEFAULT 1,
created_at TEXT DEFAULT (datetime('now')),
deprecated_at TEXT,
UNIQUE(name, version)
);

CREATE TABLE IF NOT EXISTS reviews (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
target_type TEXT NOT NULL,
target_id TEXT NOT NULL,
reviewer_role TEXT DEFAULT 'reviewer' CHECK (reviewer_role IN ('author', 'reviewer', 'agent', 'public')),
reviewer_model TEXT,
assessment TEXT NOT NULL,
recommendation TEXT CHECK (recommendation IN ('accept', 'minor_revision', 'major_revision', 'reject')),
confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
issues TEXT DEFAULT '[]',
is_blind INTEGER DEFAULT 1,
created_at TEXT DEFAULT (datetime('now')),
prompt_id TEXT REFERENCES prompts(id)
);

CREATE TABLE IF NOT EXISTS claims (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
claim_id TEXT UNIQUE NOT NULL,
statement TEXT NOT NULL,
type TEXT NOT NULL,
status TEXT DEFAULT 'open' CHECK (status IN ('verified', 'calibrated', 'predicted', 'open', 'withdrawn', 'rectified')),
evidence TEXT DEFAULT 'E' CHECK (evidence IN ('A', 'A-', 'B', 'C', 'D', 'E')),
confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
sigma REAL,
dependencies TEXT DEFAULT '[]',
since_version TEXT,
superseded_by TEXT,
withdrawn_date TEXT,
embedding BLOB,
notes TEXT,
created_at TEXT DEFAULT (datetime('now')),
updated_at TEXT DEFAULT (datetime('now')),
last_synced_at TEXT
);

CREATE TABLE IF NOT EXISTS equations (
id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))),
equation_id TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
latex TEXT NOT NULL,
latex_display TEXT,
description TEXT,
domain TEXT,
theorem_ref TEXT,
embedding BLOB,
depends_on TEXT DEFAULT '[]',
used_in_claims TEXT DEFAULT '[]',
verified INTEGER DEFAULT 0,
verification_script TEXT,
created_at TEXT DEFAULT (datetime('now')),
updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agent_roles (
role_id TEXT PRIMARY KEY,
name TEXT,
capabilities TEXT,
scope TEXT,
created_at TEXT,
retired_at TEXT,
performance_metrics TEXT
);

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_experiments_study ON experiments(study_id);
CREATE INDEX IF NOT EXISTS idx_runs_experiment ON runs(experiment_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_study ON artifacts(study_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_run ON artifacts(run_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
CREATE INDEX IF NOT EXISTS idx_claims_evidence ON claims(evidence);
CREATE INDEX IF NOT EXISTS idx_claims_superseded_by ON claims(superseded_by);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);

-- FTS5 for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS claims_fts USING fts5(
claim_id, statement, type, notes,
content='claims', content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS equations_fts USING fts5(
equation_id, name, description, latex,
content='equations', content_rowid='rowid'
);

-- Triggers for FTS sync
CREATE TRIGGER IF NOT EXISTS claims_ai AFTER INSERT ON claims BEGIN
INSERT INTO claims_fts(rowid, claim_id, statement, type, notes)
VALUES (new.rowid, new.claim_id, new.statement, new.type, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS claims_ad AFTER DELETE ON claims BEGIN
INSERT INTO claims_fts(claims_fts, rowid, claim_id, statement, type, notes)
VALUES('delete', old.rowid, old.claim_id, old.statement, old.type, old.notes);
END;

-- Updated_at triggers
CREATE TRIGGER IF NOT EXISTS tr_studies_updated AFTER UPDATE ON studies
BEGIN UPDATE studies SET updated_at = datetime('now') WHERE id = NEW.id; END;

CREATE TRIGGER IF NOT EXISTS tr_claims_updated AFTER UPDATE ON claims
BEGIN UPDATE claims SET updated_at = datetime('now') WHERE id = NEW.id; END;

CREATE TRIGGER IF NOT EXISTS tr_equations_updated AFTER UPDATE ON equations
BEGIN UPDATE equations SET updated_at = datetime('now') WHERE id = NEW.id; END;

-- VIEWS
CREATE VIEW IF NOT EXISTS claims_summary AS
SELECT evidence, status, COUNT(*) as count
FROM claims GROUP BY evidence, status ORDER BY evidence, status;

CREATE VIEW IF NOT EXISTS active_research AS
SELECT s.id, s.title, COUNT(DISTINCT e.id) as experiments, COUNT(DISTINCT r.id) as runs
FROM studies s
LEFT JOIN experiments e ON e.study_id = s.id
LEFT JOIN runs r ON r.experiment_id = e.id
WHERE s.status = 'active'
GROUP BY s.id, s.title;

-- Metadata table
CREATE TABLE IF NOT EXISTS _metadata (
key TEXT PRIMARY KEY,
value TEXT,
updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS version_history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
claim_id TEXT NOT NULL,
version TEXT NOT NULL,
change_type TEXT NOT NULL,
old_value TEXT,
new_value TEXT,
changed_by TEXT,
reason TEXT,
timestamp TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_version_history_claim_id ON version_history(claim_id);
CREATE INDEX IF NOT EXISTS idx_version_history_timestamp ON version_history(timestamp);

CREATE TABLE IF NOT EXISTS correction_queue (
id INTEGER PRIMARY KEY AUTOINCREMENT,
claim_id TEXT NOT NULL,
field TEXT NOT NULL,
old_value TEXT,
new_value TEXT NOT NULL,
evidence_category TEXT,
status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'applied', 'rejected')),
reason TEXT,
created_by TEXT,
created_at TEXT DEFAULT (datetime('now')),
applied_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_correction_queue_status ON correction_queue(status);

INSERT OR REPLACE INTO _metadata (key, value) VALUES
('schema_version', '1.0.0'),
('uidt_version', '3.7.2'),
('created_at', datetime('now'));

SELECT 'UIDT-OS SQLite schema created successfully!' as result;
