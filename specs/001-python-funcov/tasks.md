# Tasks: Python Functional Coverage Tool

**Feature**: 001-python-funcov
**Generated**: 2026-02-14

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 36 |
| User Story 1 (P1) | 9 tasks |
| User Story 2 (P2) | 6 tasks |
| User Story 3 (P3) | 6 tasks |

---

## Phase 1: Setup

- [X] T001 Create project structure per implementation plan (src/pyfuncov/, tests/, pyproject.toml)
- [X] T002 Create pyproject.toml with project metadata and dependencies in pyproject.toml
- [X] T003 Initialize uv environment and generate uv.lock file using `uv lock` in project root
- [X] T004 Install dependencies using `uv sync` in project root

---

## Phase 2: Foundational

- [X] T005 [P] Create BinKind enum in src/pyfuncov/models/enums.py
- [X] T006 [P] Create OutOfBoundsMode enum in src/pyfuncov/models/enums.py
- [X] T007 Create Bin dataclass with fields (name, bin_type, value, range_min, range_max, from_value, to_value, hits, last_hit) in src/pyfuncov/models/bin.py
- [X] T008 Create Coverpoint dataclass with fields (name, bins, type, out_of_bounds) in src/pyfuncov/models/coverpoint.py
- [X] T009 Create Covergroup dataclass with fields (name, coverpoints, module, created_at) in src/pyfuncov/models/covergroup.py
- [X] T010 Create CoverageData dataclass for accumulated hits in src/pyfuncov/models/coverage_data.py

---

## Phase 3: User Story 1 - Define and Track Coverage Points (P1)

**Goal**: Enable users to define covergroups, coverpoints, and bins, then sample values against them.

**Independent Test**: Create coverpoints and covergroups with various bins (specific values, ranges, transitions), then verify they are correctly registered and can be sampled.

**Implementation**:

- [X] T011 [P] [US1] Implement Bin.match_discrete() method to check if value matches discrete bin in src/pyfuncov/models/bin.py
- [X] T012 [P] [US1] Implement Bin.match_range() method to check if value falls within range bin in src/pyfuncov/models/bin.py
- [X] T013 [US1] Implement Covergroup.sample() method to sample a value and find matching bin in src/pyfuncov/models/covergroup.py
- [X] T014 [US1] Add Covergroup.add_coverpoint() to add coverpoints with bins in src/pyfuncov/models/covergroup.py
- [X] T015 [US1] Add Covergroup.register() to register covergroup globally in src/pyfuncov/models/covergroup.py
- [X] T016 [US1] Handle out-of-bounds values (ignore/warn/error) per OutOfBoundsMode in src/pyfuncov/models/covergroup.py
- [X] T017 [US1] Add transition tracking (previous value state) for transition bins in src/pyfuncov/models/covergroup.py
- [X] T018 [US1] Validate bin definitions per data-model.md (non-empty names, range_min <= range_max, from_value != to_value) in src/pyfuncov/models/
- [X] T019 [US1] Write unit tests for discrete bin matching in tests/unit/test_bin.py
- [X] T020 [US1] Write unit tests for range bin matching in tests/unit/test_bin.py

---

## Phase 4: User Story 2 - Collect Coverage Across Test Runs (P2)

**Goal**: Enable persistence and aggregation of coverage data across multiple test runs.

**Independent Test**: Run a test that samples coverage points, then verify the coverage data is persisted and can be loaded.

**Implementation**:

- [X] T021 [P] [US2] Implement JSON storage for CoverageData in src/pyfuncov/storage/json_storage.py
- [X] T022 [US2] Implement save_coverage() function to persist data in src/pyfuncov/storage/__init__.py
- [X] T023 [US2] Implement load_coverage() function to load persisted data in src/pyfuncov/storage/__init__.py
- [X] T024 [US2] Implement cumulative aggregation when loading existing data in src/pyfuncov/storage/json_storage.py
- [X] T025 [US2] Handle corrupted/incomplete coverage data files gracefully with warning (per spec clarification) in src/pyfuncov/storage/json_storage.py
- [X] T026 [US2] Implement module namespacing for covergroup name collision prevention in src/pyfuncov/models/covergroup.py
- [X] T027 [US2] Write integration tests for persistence and aggregation in tests/integration/test_persistence.py

---

## Phase 5: User Story 3 - Analyze Coverage Gaps (P3)

**Goal**: Generate coverage reports to identify untested edge cases.

**Independent Test**: Create coverage definitions, sample partial values, then generate a report that correctly shows hit vs. missed bins.

**Implementation**:

- [X] T028 [P] [US3] Implement text report generation with coverage percentages in src/pyfuncov/core/report.py
- [X] T029 [US3] Implement JSON report generation for CI/CD integration in src/pyfuncov/core/report.py
- [X] T030 [US3] Implement coverage comparison (diff) between two runs in src/pyfuncov/core/report.py
- [X] T031 [US3] Calculate per-covergroup and overall coverage percentages in src/pyfuncov/core/report.py
- [X] T032 [US3] List missed bins in reports in src/pyfuncov/core/report.py
- [X] T033 [US3] Write tests for report generation in tests/unit/test_report.py

---

## Phase 6: Polish & CLI

**Implementation**:

- [X] T034 [P] Create src/pyfuncov/__init__.py with public API exports (Covergroup, Coverpoint, BinKind, OutOfBoundsMode, save_coverage, load_coverage, generate_report)
- [X] T035 [P] Configure pytest in pyproject.toml (testpaths, python_files, python_classes, python_functions)
- [X] T036 Create tests/conftest.py with pytest fixtures for coverage integration in tests/conftest.py
- [X] T037 Create CLI entry point in src/pyfuncov/cli/__init__.py
- [X] T038 Add 'report' CLI command to generate text/JSON reports
- [X] T039 Add 'diff' CLI command to compare coverage runs
- [X] T040 Verify pyfuncov's own test coverage meets quality standards in tests/
- [X] T041 Run final integration tests in tests/integration/

---

## Dependencies

```
Setup (Phase 1)
    ↓
Foundational (Phase 2) ← US1 depends on models/enums.py
    ↓
US1 (Phase 3) ← Builds on foundational models
    ↓
US2 (Phase 4) ← Depends on US1 (needs sample logic)
    ↓
US3 (Phase 5) ← Depends on US2 (needs data to report)
    ↓
Polish (Phase 6)
```

**Parallel Execution Opportunities**:
- Phase 2 tasks T005-T006 (enums) can run in parallel
- Phase 3 tasks T011-T012 (bin matching methods) can run in parallel
- Phase 4 tasks T021 (JSON storage) is independent
- Phase 6 tasks T034-T036 (API exports, pytest config, conftest) can run in parallel

---

## MVP Scope

**Recommended MVP**: User Story 1 only (Phase 3)
- This provides the core value: defining and sampling coverage points
- Can be tested independently
- Enables iterative delivery

---

## Implementation Strategy

1. **MVP First**: Implement Phase 1-3 (US1) to get core functionality working
2. **Incremental Delivery**: Add Phase 4 (US2) for persistence, then Phase 5 (US3) for reporting
3. **Polish Last**: CLI and final integration tests in Phase 6
