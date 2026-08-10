import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { searchWorkspacePages } from "../api/pages";
import "./SearchModal.css";

function SearchModal({ open, onClose, workspaceId, onSelectPage }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!open) {
      setQuery("");
      setResults([]);
    }
  }, [open]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const data = await searchWorkspacePages(workspaceId, query);

        setResults(data);
      } catch {
        toast.error("Search failed");
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query, workspaceId]);

  if (!open) return null;

  return (
    <div className="search-overlay">
      <div className="search-modal">
        <input
          autoFocus
          placeholder="Search pages..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="search-results">
          {results.length === 0 ? (
            <p>No pages found</p>
          ) : (
            results.map((page) => (
              <button
                key={page.id}
                onClick={() => {
                  onSelectPage(page);
                  onClose();
                }}
              >
                <strong>{page.title}</strong>
              </button>
            ))
          )}
        </div>

        <button className="close-btn" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

export default SearchModal;
