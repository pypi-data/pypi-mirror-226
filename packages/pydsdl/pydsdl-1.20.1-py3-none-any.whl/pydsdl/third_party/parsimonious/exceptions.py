from textwrap import dedent

from parsimonious.utils import StrAndRepr


class ParsimoniousError(Exception):
    """A base exception class to allow library users to catch any Parsimonious error."""
    pass


class ParseError(StrAndRepr, ParsimoniousError):
    """A call to ``Expression.parse()`` or ``match()`` didn't match."""

    def __init__(self, text, pos=-1, expr=None):
        # It would be nice to use self.args, but I don't want to pay a penalty
        # to call descriptors or have the confusion of numerical indices in
        # Expression.match_core().
        self.text = text
        self.pos = pos
        self.expr = expr

    def __str__(self):
        rule_name = (("'%s'" % self.expr.name) if self.expr.name else
                     str(self.expr))
        return "Rule %s didn't match at '%s' (line %s, column %s)." % (
                rule_name,
                self.text[self.pos:self.pos + 20],
                self.line(),
                self.column())

    # TODO: Add line, col, and separated-out error message so callers can build
    # their own presentation.

    def line(self):
        """Return the 1-based line number where the expression ceased to
        match."""
        # This is a method rather than a property in case we ever wanted to
        # pass in which line endings we want to use.
        if isinstance(self.text, list):  # TokenGrammar
            return None
        else:
            return self.text.count('\n', 0, self.pos) + 1

    def column(self):
        """Return the 1-based column where the expression ceased to match."""
        # We choose 1-based because that's what Python does with SyntaxErrors.
        try:
            return self.pos - self.text.rindex('\n', 0, self.pos)
        except (ValueError, AttributeError):
            return self.pos + 1


class LeftRecursionError(ParseError):
    def __str__(self):
        rule_name = self.expr.name if self.expr.name else str(self.expr)
        window = self.text[self.pos:self.pos + 20]
        return dedent(f"""
            Left recursion in rule {rule_name!r} at {window!r} (line {self.line()}, column {self.column()}).

            Parsimonious is a packrat parser, so it can't handle left recursion.
            See https://en.wikipedia.org/wiki/Parsing_expression_grammar#Indirect_left_recursion
            for how to rewrite your grammar into a rule that does not use left-recursion.
            """
        ).strip()


class IncompleteParseError(ParseError):
    """A call to ``parse()`` matched a whole Expression but did not consume the
    entire text."""

    def __str__(self):
        return "Rule '%s' matched in its entirety, but it didn't consume all the text. The non-matching portion of the text begins with '%s' (line %s, column %s)." % (
                self.expr.name,
                self.text[self.pos:self.pos + 20],
                self.line(),
                self.column())


class VisitationError(ParsimoniousError):
    """Something went wrong while traversing a parse tree.

    This exception exists to augment an underlying exception with information
    about where in the parse tree the error occurred. Otherwise, it could be
    tiresome to figure out what went wrong; you'd have to play back the whole
    tree traversal in your head.

    """
    # TODO: Make sure this is pickleable. Probably use @property pattern. Make
    # the original exc and node available on it if they don't cause a whole
    # raft of stack frames to be retained.
    def __init__(self, exc, exc_class, node):
        """Construct.

        :arg exc: What went wrong. We wrap this and add more info.
        :arg node: The node at which the error occurred

        """
        self.original_class = exc_class
        super().__init__(
            '%s: %s\n\n'
            'Parse tree:\n'
            '%s' %
            (exc_class.__name__,
             exc,
             node.prettily(error=node)))


class BadGrammar(StrAndRepr, ParsimoniousError):
    """Something was wrong with the definition of a grammar.

    Note that a ParseError might be raised instead if the error is in the
    grammar definition syntax.

    """


class UndefinedLabel(BadGrammar):
    """A rule referenced in a grammar was never defined.

    Circular references and forward references are okay, but you have to define
    stuff at some point.

    """
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return 'The label "%s" was never defined.' % self.label
