import "katex/dist/katex.min.css";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

interface MathTextProps {
  content: string;
  className?: string;
}

function normalizeMathContent(content: string): string {
  let normalized = content;

  // Convert LaTeX delimiters to remark-math friendly delimiters.
  normalized = normalized.replace(/\\\[(.*?)\\\]/gs, (_, expr: string) => `$$\n${expr.trim()}\n$$`);
  normalized = normalized.replace(/\\\((.*?)\\\)/gs, (_, expr: string) => `$${expr.trim()}$`);

  // Convert full-line bracket formulas like: [ S_n = \frac{n(n+1)}{2} ]
  normalized = normalized.replace(/^\s*\[(.+)\]\s*$/gm, (line: string, expr: string) => {
    const looksMath = /\\|\^|_|=|\d+\s*[+\-*/]/.test(expr);
    if (!looksMath) {
      return line;
    }
    return `$$\n${expr.trim()}\n$$`;
  });

  // Normalize $$ blocks so delimiters sit on their own lines.
  normalized = normalized.replace(/([^\n])\$\$/g, "$1\n$$");
  normalized = normalized.replace(/\$\$([^\n])/g, "$$\n$1");

  // Ensure $$ blocks are balanced across the whole response.
  const lines = normalized.split("\n");
  let inBlock = false;
  normalized = lines
    .map((line, idx) => {
      const blockCount = (line.match(/\$\$/g) || []).length;
      if (blockCount % 2 === 1) {
        inBlock = !inBlock;
      }
      if (idx === lines.length - 1 && inBlock) {
        return `${line}\n$$`;
      }
      return line;
    })
    .join("\n");

  // Balance inline $ delimiters per line by escaping a dangling $ when needed.
  normalized = normalized
    .split("\n")
    .map((line) => {
      const withoutBlocks = line.replace(/\$\$[^$]*\$\$/g, "");
      const singleDollarCount = (withoutBlocks.match(/(?<!\\)\$/g) || []).length;
      if (singleDollarCount % 2 === 1) {
        const lastIndex = line.lastIndexOf("$");
        if (lastIndex >= 0) {
          return `${line.slice(0, lastIndex)}\\${line.slice(lastIndex)}`;
        }
      }
      return line;
    })
    .join("\n");

  return normalized.trim();
}

export function MathText({ content, className = "" }: MathTextProps) {
  return (
    <div className={`MathText-container ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[[rehypeKatex, { throwOnError: false, errorColor: "var(--color-text-danger)", strict: "ignore" }]]}
        components={{
          code({ children }) {
            return <>{children}</>;
          },
          p({ children }) {
            return <p className="m-0 leading-relaxed text-inherit">{children}</p>;
          },
          strong({ children }) {
            return <>{children}</>;
          },
        }}
      >
        {normalizeMathContent(content)}
      </ReactMarkdown>
    </div>
  );
}
