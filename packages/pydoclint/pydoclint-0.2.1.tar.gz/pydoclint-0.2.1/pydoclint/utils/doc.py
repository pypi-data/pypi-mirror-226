from typing import Any, List

import docstring_parser.parser as sphinx_parser
from docstring_parser.common import Docstring, DocstringReturns
from docstring_parser.google import GoogleParser
from numpydoc.docscrape import NumpyDocString

from pydoclint.utils.arg import ArgList
from pydoclint.utils.internal_error import InternalError
from pydoclint.utils.return_arg import ReturnArg
from pydoclint.utils.yield_arg import YieldArg


class Doc:
    """A class to hold docstring and to provide info on the parsed docstring"""

    def __init__(self, docstring: str, style: str = 'numpy') -> None:
        self.docstring = docstring
        self.style = style

        if style == 'numpy':
            # Note: a NumpyDocString object has the following sections:
            # *  {'Signature': '', 'Summary': [''], 'Extended Summary': [],
            # *  'Parameters': [], 'Returns': [], 'Yields': [], 'Receives': [],
            # *  'Raises': [], 'Warns': [], 'Other Parameters': [],
            # *  'Attributes': [], 'Methods': [], 'See Also': [], 'Notes': [],
            # *  'Warnings': [], 'References': '', 'Examples': '', 'index': {}}
            self.parsed = NumpyDocString(docstring)
        elif style == 'google':
            parser = GoogleParser()
            self.parsed = parser.parse(docstring)
        elif style == 'sphinx':
            self.parsed = sphinx_parser.parse(docstring)
        else:
            self._raiseException()

    @property
    def isShortDocstring(self) -> bool:
        """Is the docstring a short one (containing only a summary)"""
        if self.style == 'numpy':
            return (
                (
                    bool(self.parsed.get('Summary'))
                    or bool(self.parsed.get('Extended Summary'))
                )
                and not bool(self.parsed.get('Parameters'))
                and not bool(self.parsed.get('Returns'))
                and not bool(self.parsed.get('Yields'))
                and not bool(self.parsed.get('Receives'))
                and not bool(self.parsed.get('Raises'))
                and not bool(self.parsed.get('Warns'))
                and not bool(self.parsed.get('Other Parameters'))
                and not bool(self.parsed.get('Attributes'))
                and not bool(self.parsed.get('Methods'))
                and not bool(self.parsed.get('See Also'))
                and not bool(self.parsed.get('Notes'))
                and not bool(self.parsed.get('Warnings'))
                and not bool(self.parsed.get('References'))
                and not bool(self.parsed.get('Examples'))
                and not bool(self.parsed.get('index'))
            )

        if self.style in {'google', 'sphinx'}:
            # API documentation:
            # https://rr-.github.io/docstring_parser/docstring_parser.Docstring.html
            return (
                (
                    bool(self.parsed.short_description)
                    or bool(self.parsed.long_description)
                )
                and len(self.parsed.params) == 0
                and len(self.parsed.raises) == 0
                and self.parsed.returns is None
                and len(self.parsed.many_returns) == 0
                and len(self.parsed.examples) == 0
                and self.parsed.deprecation is None
            )

        self._raiseException()  # noqa: R503

    @property
    def argList(self) -> ArgList:
        """The argument info in the docstring, presented as an ArgList"""
        if self.style == 'numpy':
            return ArgList.fromNumpydocParam(self.parsed.get('Parameters', []))

        if self.style in {'google', 'sphinx'}:
            return ArgList.fromGoogleParsedParam(self.parsed.params)

        self._raiseException()  # noqa: R503

    @property
    def hasReturnsSection(self) -> bool:
        """Whether the docstring has a 'Returns' section"""
        if self.style == 'numpy':
            return bool(self.parsed.get('Returns'))

        if self.style in {'google', 'sphinx'}:
            retSection: DocstringReturns = self.parsed.returns
            return retSection is not None and not retSection.is_generator

        self._raiseException()  # noqa: R503

    @property
    def hasYieldsSection(self) -> bool:
        """Whether the docstring has a 'Yields' section"""
        if self.style == 'numpy':
            return bool(self.parsed.get('Yields'))

        if self.style in {'google', 'sphinx'}:
            retSection: DocstringReturns = self.parsed.returns
            return retSection is not None and retSection.is_generator

        self._raiseException()  # noqa: R503

    @property
    def hasRaisesSection(self) -> bool:
        """Whether the docstring has a 'Raises' section"""
        if self.style == 'numpy':
            return bool(self.parsed.get('Raises'))

        if self.style in {'google', 'sphinx'}:
            return len(self.parsed.raises) > 0

        self._raiseException()  # noqa: R503

    @property
    def returnSection(self) -> List[ReturnArg]:
        """Get the return section of the docstring"""
        if isinstance(self.parsed, Docstring):  # Google style
            returnArg = ReturnArg(
                argName=self._str(self.parsed.returns.return_name),
                argType=self._str(self.parsed.returns.type_name),
                argDescr=self._str(self.parsed.returns.description),
            )
            return [returnArg]  # Google style always has only 1 return arg

        if isinstance(self.parsed, NumpyDocString):  # numpy style
            returnSection = self.parsed.get('Returns')
            result = []
            for element in returnSection:
                result.append(
                    ReturnArg(
                        argName=self._str(element.name),
                        argType=self._str(element.type),
                        argDescr=' '.join(element.desc),
                    )
                )

            return result

        return []

    @property
    def yieldSection(self) -> List[YieldArg]:
        """Get the yield section of the docstring"""
        if isinstance(self.parsed, Docstring):  # Google or Sphinx style
            yieldArg = YieldArg(
                argName=self._str(self.parsed.returns.return_name),
                argType=self._str(self.parsed.returns.type_name),
                argDescr=self._str(self.parsed.returns.description),
            )
            return [yieldArg]  # Google/Sphinx style always has only 1 yield arg

        if isinstance(self.parsed, NumpyDocString):  # numpy style
            yieldSection = self.parsed.get('Yields')
            result = []
            for element in yieldSection:
                result.append(
                    YieldArg(
                        argName=self._str(element.name),
                        argType=self._str(element.type),
                        argDescr=' '.join(element.desc),
                    )
                )

            return result

        return []

    def _raiseException(self) -> None:
        msg = f'Unknown style "{self.style}"; please contact the authors'
        raise InternalError(msg)

    @classmethod
    def _str(cls, something: Any) -> str:
        return '' if something is None else str(something)
