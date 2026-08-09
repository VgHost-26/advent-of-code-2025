import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const SolutionViewer = ({ code, language, highlightRanges }) => {
    const isLineHighlighted = (lineNumber) => {
        if (!highlightRanges || highlightRanges.length === 0) return true;

        // Ranges are 0-indexed in our JSON, but lineNumber is 1-indexed usually?
        // Wait, let's check update_progress.py. 
        // enumerate(lines) is 0-indexed.
        // current_start = i + 1 (so 0-indexed line i becomes 1-indexed start?)
        // highlight_ranges.append([current_start, i]) -> i is 0-indexed index of the line BEFORE the end marker.

        // Let's re-verify update_progress.py logic:
        // if start_marker in stripped: current_start = i + 1. 
        //    Example: line 5 has marker. i=5. current_start=6.
        //    So line 6 (0-indexed) is the first line of code.
        // if end_marker in stripped: highlight_ranges.append([current_start, i])
        //    Example: line 10 has marker. i=10. range is [6, 10].
        //    This means lines 6, 7, 8, 9. (Python range style: start inclusive, end exclusive).

        // SyntaxHighlighter usually treats lines as 1-indexed for display, but let's see how lineProps works.
        // Usually lineProps receives lineNumber starting from 1.

        // Let's adjust logic to be 1-based for simplicity in comparison if SyntaxHighlighter uses 1-based.
        // If our range is [6, 10] (0-based indices 6,7,8,9), that corresponds to 1-based lines 7,8,9,10.

        // Let's look at update_progress.py again.
        // current_start = i + 1. If marker is at 0-based index 5 (line 6), current_start is 6.
        // range [6, 10] means lines with 0-based index 6, 7, 8, 9.
        // These are 1-based lines 7, 8, 9, 10.

        // So if lineNumber (1-based) is passed:
        // We need to check if (lineNumber - 1) is >= start and < end.

        const lineIndex = lineNumber - 1;
        return highlightRanges.some(([start, end]) => lineIndex >= start && lineIndex < end);
    };

    return (
        <div className="overflow-hidden">
            <SyntaxHighlighter
                language={language}
                style={vscDarkPlus}
                showLineNumbers={true}
                wrapLines={true}
                lineProps={(lineNumber) => {
                    const isHighlighted = isLineHighlighted(lineNumber);
                    return {
                        style: {
                            opacity: isHighlighted ? 1 : 0.3,
                            transition: 'opacity 0.3s',
                            display: 'block'
                        }
                    };
                }}
                customStyle={{
                    margin: 0,
                    padding: '1.5rem',
                    fontSize: '0.9rem',
                    lineHeight: '1.5',
                }}
            >
                {code}
            </SyntaxHighlighter>
        </div>
    );
};

export default SolutionViewer;
