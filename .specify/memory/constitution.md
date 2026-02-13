<!--
  Sync Impact Report
  ==================
  Version change: 1.3.0 → 1.4.0 (MINOR)
  Added principles:
    - VIII. Explicit Domain States
  Modified sections:
    - Governance: Compliance Verification updated to include explicit domain state validation
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md: ✅ already aligned
    - .specify/templates/spec-template.md: ✅ already aligned
    - .specify/templates/tasks-template.md: ✅ already aligned
  Follow-up TODOs: None
-->

# pyfuncov Constitution

## Core Principles

### I. Test-First Development

For any bug fix or feature change, failing tests MUST be written first to demonstrate the current incorrect behavior before any implementation begins.

If any test that is expected to fail passes, the agent MUST stop and explain the contradiction before proceeding with implementation.

**Rationale**: Test-first ensures regressions are caught early, provides living documentation of expected behavior, and guarantees that fixes are verifiable. Requiring explanation of unexpected test results prevents silent failures that could introduce subtle bugs.

### II. Architectural Integrity

The codebase MUST maintain single sources of truth with no duplicate logic paths or parallel handlers for the same rule.

#### Rules

- No duplicate logic paths: Business logic MUST exist in exactly one location
- No parallel handlers: Each rule or behavior MUST have one authoritative implementation
- No bypassing single sources of truth: All access to shared state, configurations, or business rules MUST flow through designated entry points

**Rationale**: Duplicate logic leads to divergent implementations that are difficult to maintain and synchronize. Single sources of truth ensure consistency, simplify debugging, and make changes auditable.

### III. Test Coverage Quality

All public APIs and core functionality MUST have corresponding tests. Coverage tools and their outputs MUST be validated for accuracy.

#### Coverage Rules

- Unit tests MUST cover all public functions and classes
- Integration tests MUST verify component interactions
- Coverage reports MUST accurately reflect actual code execution
- Edge cases in coverage logic MUST have explicit tests

**Rationale**: For a coverage tool project, accurate measurement is foundational. Poor coverage validation undermines the tool's reliability and user trust.

### IV. Documentation Standards

All public APIs MUST have docstrings explaining purpose, parameters, return values, and examples.

#### Documentation Rules

- Public functions MUST have docstrings with type hints
- Complex logic MUST include inline comments explaining intent
- README and user-facing docs MUST stay synchronized with code
- Breaking changes MUST be documented in changelog

**Rationale**: Documentation enables collaboration, reduces onboarding time, and serves as a contract for API consumers.

### V. Simplicity First

Start with the simplest implementation that satisfies requirements. Avoid over-engineering and YAGNI (You Aren't Gonna Need It) constructs.

#### Simplicity Rules

- Prefer simple solutions over clever ones
- Delay complexity until proven necessary
- Remove dead code and unused features
- Refactor toward simplicity after each iteration

**Rationale**: Simple code is easier to maintain, debug, and extend. Premature abstraction creates maintenance burden.

### VI. Timeout Safety

All loops MUST have a maximum iteration bound to prevent infinite loops. All wait operations, timeouts, and blocking calls MUST have explicit timeout values.

#### Timeout Rules

- All loops MUST have a defined termination condition with a maximum iteration count
- All wait operations (e.g., polling, async waits, event loops) MUST have explicit timeouts
- Timeouts MUST be configurable with sensible defaults
- Infinite loops MUST be replaced with bounded loops with explicit exit conditions
- Timeout exceptions MUST be caught and handled gracefully

**Rationale**: Unbounded loops and waits can cause processes to hang indefinitely, making debugging difficult and causing reliability issues in production. Explicit bounds ensure predictable behavior and faster failure detection.

### VII. Fail-Fast Strict Mode

Fallback behavior is FORBIDDEN. If required data is missing, the system MUST fail fast and report an error immediately. Producing a default or probabilistic behavior to mask missing data is NOT allowed. Any such failure MUST be fixed in the caller, not the callee.

#### Fail-Fast Rules

- Missing required data MUST raise explicit errors, not return defaults
- Functions MUST validate all required inputs before proceeding
- Silent fallbacks, magic values, or probabilistic outputs MUST NOT be used to handle missing data
- Errors MUST include context about what data was missing and where
- Callers MUST be responsible for providing required data; callees MUST NOT guess

**Rationale**: Hidden fallbacks create fragile systems where bugs manifest far from their source. Fail-fast debugging is faster and more reliable. Making callers responsible for providing data ensures the contract is explicit and traceable.

### VIII. Explicit Domain States

None/null values MUST ONLY represent the absence of a value (e.g., no return value, missing lookup result, invalid reference). They MUST NOT encode domain meaning or outcomes. Distinct domain states (e.g., skip, tie, no-op, pending decision, neutral result) MUST have explicit, distinguishable representations.

#### Domain State Rules

- None/null MUST NOT be used to convey domain semantics (e.g., "no decision made", "result skipped", "tie occurred")
- Distinct domain states MUST be represented with explicit types (e.g., enums, dataclasses, Result patterns)
- Functions that can return domain-meaningful "nothing" states MUST return explicit types, not None
- Any use of None to convey domain semantics is a constitutional violation

**Rationale**: Using None for domain semantics creates ambiguous code where the meaning of "no value" is unclear. Explicit domain types make code self-documenting, enable exhaustive pattern matching, and prevent silent bugs from misinterpreted nulls.

### Testing Discipline

- Unit tests MUST cover all public APIs and pure functions
- Integration tests MUST verify component interactions
- Contract tests MUST validate interfaces between modules
- Tests MUST be self-contained and independent (no order dependencies)

### Code Organization

- Files MUST have a single responsibility
- Functions MUST be small and do one thing well
- Dependencies MUST be explicit and minimized
- Configuration MUST be externalized (no magic numbers or strings)

## Development Workflow

### Pre-Implementation Requirements

Before writing any feature code:
1. Write failing test(s) that demonstrate the desired behavior
2. Verify the test(s) fail with the current implementation
3. Document the expected behavior in the test comments

### Implementation Requirements

- Implement only what is necessary to pass the failing test(s)
- Refactor after tests pass (Red-Green-Refactor cycle)
- Do not introduce new functionality while fixing a bug

### Review Requirements

- All changes MUST include corresponding tests
- Code review MUST verify architectural integrity
- Reviewers MUST check for duplicate logic and parallel handlers

## Governance

**Constitution Precedence**: This constitution supersedes all other development practices. When conflicts arise, constitutional principles take precedence.

**Amendment Procedure**: Changes to this constitution require:
1. Documentation of the proposed change
2. Rationale explaining why the change is necessary
3. Impact assessment on existing code
4. Review and approval by project maintainers

**Compliance Verification**: All pull requests MUST verify compliance with these principles. The review process MUST include checks for:
- Test-first adherence (failing tests before implementation)
- Architectural integrity (no duplicate logic, no parallel handlers)
- Single source of truth enforcement
- Timeout safety (bounded loops, explicit timeouts)
- Fail-fast validation (no fallback behavior for missing data)
- Explicit domain state validation (None only represents absence of value)

**Version**: 1.4.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-13
