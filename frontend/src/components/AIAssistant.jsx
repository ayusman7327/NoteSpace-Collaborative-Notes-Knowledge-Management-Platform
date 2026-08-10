import { useState } from "react";
import toast from "react-hot-toast";

import { askAI } from "../api/ai";
import "./AIAssistant.css";

function AIAssistant({ open, onClose, editor, pageTitle }) {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const getPageContent = () => {
    if (!editor) {
      return "";
    }

    return editor.getText();
  };

  const runAI = async (instruction) => {
    if (!editor) {
      toast.error("Editor is not available");
      return;
    }

    const content = getPageContent();

    if (!content.trim()) {
      toast.error("Write something in the page first");
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const fullPrompt = `
You are the AI assistant inside NoteSpace, a collaborative knowledge management application.

Page title:
${pageTitle || "Untitled"}

Page content:
${content}

Task:
${instruction}

Return only the useful final result.
`;

      const result = await askAI(fullPrompt);

      setResponse(result);
    } catch (error) {
      console.error(error);

      toast.error(error.response?.data?.detail || "AI assistant failed");
    } finally {
      setLoading(false);
    }
  };

  const handleCustomPrompt = async (event) => {
    event.preventDefault();

    const cleanedPrompt = prompt.trim();

    if (!cleanedPrompt) {
      toast.error("Enter a request for AI");
      return;
    }

    await runAI(cleanedPrompt);
  };

  const insertResponse = () => {
    if (!editor || !response) {
      return;
    }

    editor
      .chain()
      .focus()
      .insertContent(`<p>${response.replace(/\n/g, "</p><p>")}</p>`)
      .run();

    toast.success("AI response added to page");
  };

  const replacePageContent = () => {
    if (!editor || !response) {
      return;
    }

    editor.commands.setContent(`<p>${response.replace(/\n/g, "</p><p>")}</p>`);

    toast.success("Page updated with AI response");
  };

  if (!open) {
    return null;
  }

  return (
    <aside className="ai-assistant">
      <div className="ai-header">
        <div className="ai-brand">
          <div className="ai-logo">✦</div>

          <div>
            <strong>NoteSpace AI</strong>

            <span>Writing assistant</span>
          </div>
        </div>

        <button type="button" className="ai-close" onClick={onClose}>
          ×
        </button>
      </div>

      <div className="ai-body">
        <div className="ai-intro">
          <span>AI ASSISTANT</span>

          <h2>Improve your notes</h2>

          <p>
            Summarize, rewrite, explain, or generate structured content from the
            current page.
          </p>
        </div>

        <div className="ai-actions">
          <button
            type="button"
            onClick={() =>
              runAI(
                "Summarize this page clearly and concisely. Keep the important points.",
              )
            }
          >
            <span>✦</span>

            <div>
              <strong>Summarize</strong>

              <small>Create a concise summary</small>
            </div>
          </button>

          <button
            type="button"
            onClick={() =>
              runAI(
                "Rewrite this content in a clear, professional and polished style without changing its meaning.",
              )
            }
          >
            <span>↗</span>

            <div>
              <strong>Rewrite</strong>

              <small>Make writing professional</small>
            </div>
          </button>

          <button
            type="button"
            onClick={() =>
              runAI(
                "Fix the grammar, spelling and sentence structure of this content.",
              )
            }
          >
            <span>✓</span>

            <div>
              <strong>Fix grammar</strong>

              <small>Improve readability</small>
            </div>
          </button>

          <button
            type="button"
            onClick={() =>
              runAI(
                "Extract all actionable tasks from this page. Return a clear checklist.",
              )
            }
          >
            <span>☑</span>

            <div>
              <strong>Action items</strong>

              <small>Extract tasks and next steps</small>
            </div>
          </button>

          <button
            type="button"
            onClick={() =>
              runAI(
                "Explain the content of this page in simple language as if teaching a beginner.",
              )
            }
          >
            <span>?</span>

            <div>
              <strong>Explain</strong>

              <small>Simplify complex ideas</small>
            </div>
          </button>

          <button
            type="button"
            onClick={() =>
              runAI(
                "Convert this content into professional meeting notes with sections for summary, key decisions, action items and follow-ups.",
              )
            }
          >
            <span>▤</span>

            <div>
              <strong>Meeting notes</strong>

              <small>Structure meeting content</small>
            </div>
          </button>
        </div>

        <div className="ai-custom-section">
          <span className="ai-section-label">Ask anything</span>

          <form onSubmit={handleCustomPrompt}>
            <textarea
              placeholder="Ask AI about this page..."
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
            />

            <button type="submit" disabled={loading}>
              {loading ? "Thinking..." : "Ask AI"}
            </button>
          </form>
        </div>

        <div className="ai-result-section">
          <div className="ai-result-header">
            <span className="ai-section-label">AI response</span>

            {response && (
              <button type="button" onClick={() => setResponse("")}>
                Clear
              </button>
            )}
          </div>

          {loading ? (
            <div className="ai-loading">
              <div />
              <div />
              <div />

              <span>NoteSpace AI is thinking...</span>
            </div>
          ) : response ? (
            <>
              <div className="ai-response">{response}</div>

              <div className="ai-response-actions">
                <button type="button" onClick={insertResponse}>
                  Add to page
                </button>

                <button
                  type="button"
                  className="ai-secondary-action"
                  onClick={replacePageContent}
                >
                  Replace page
                </button>
              </div>
            </>
          ) : (
            <div className="ai-empty-response">
              <div>✦</div>

              <p>
                Choose an AI action or ask a question about your current note.
              </p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}

export default AIAssistant;
