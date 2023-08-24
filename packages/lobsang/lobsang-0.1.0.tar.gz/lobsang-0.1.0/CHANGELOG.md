# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.0] 2023-08-16
### Added
- `chat.history` property to access the conversation history
- `data` prop for assistant messages containing parsed data from the LLM's response
- Added `example` parameter to JSONAnswer to provide an example for the LLM

### Changed 

- Rename directives to answers and simplify the interface
- Rework chat class to be more simple and easy to use
- Moved validate function to `lobsang/utils.py` (not part of this release)
- `repr(chat)` now returns string which can be used to recreate the object
- Calling chat will now throw ParseError if the response from the LLM is not valid according to the requested format

### Removed
- Removed inheritance from list of chat class
- Removed option (bloated) to call chat with a single string or multiple messages without corresponding answer
  which then would be interpolated by the chat class (confusing and not really useful)


## [0.0.5] 2023-08-07

### Fixed
- Fix version specifier in pyproject.toml

## [0.0.4] 2023-08-07

### Changed
- Switched from 'ast.literal_eval' to 'json.loads' in JSONDirective

### Removed
- Remove trailing newline from JOSONDirective.instructions

## [0.0.3] 2023-08-06

### Added

- Add abstract `instructions` property to abstract base class `Directive`
- Add _info method to easily create info dict for directive
- Add tutorial for directives
- Add OpenAI wrapper to easily use OpenAI API with lobsang

### Changed

- Implement `embed` of `Directive` to use `instructions` as template to embed message and return dict with `directive`
  and `original` keys
- Implement `parse` of `Directive` to add `directive` and `**kwargs` to returned dict (still abstractmethod)

### Removed

- Remove `directive` and `query` in `chat._invoke_with_directive` since it is now handled by `Directive` class

## [0.0.2] 2023-08-04

Keeping this short, since no one is using this yet.

### Added

- Example for basic usage of the library

### Changed

- Rework the `Chat` class to be more simple and easy to use.

### Fixed

- Fix bugs in pyproject.toml and __init__.py

## [0.0.1] 2023-07-31

Initial Release

