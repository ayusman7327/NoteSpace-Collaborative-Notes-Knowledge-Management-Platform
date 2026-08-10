import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { useAuth } from "../context/AuthContext";
import "./Auth.css";

function Login() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [submitting, setSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);

    try {
      await login(formData.email, formData.password);

      toast.success("Welcome back");
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Invalid email or password");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-shell">
      <section className="auth-showcase">
        <div className="brand-mark">N</div>

        <div className="showcase-content">
          <span className="showcase-badge">Knowledge, organized</span>

          <h1>
            Your ideas deserve
            <br />a better workspace.
          </h1>

          <p>
            Capture notes, structure knowledge, manage projects, and collaborate
            with your team — all in one focused workspace.
          </p>

          <div className="showcase-points">
            <div>
              <span>01</span>
              <p>Organize work with nested pages</p>
            </div>

            <div>
              <span>02</span>
              <p>Collaborate across shared workspaces</p>
            </div>

            <div>
              <span>03</span>
              <p>Search, tag, restore, and track changes</p>
            </div>
          </div>
        </div>

        <div className="showcase-footer">
          <span>NoteSpace</span>
          <span>Collaborative Knowledge Platform</span>
        </div>
      </section>

      <section className="auth-form-section">
        <div className="auth-card">
          <div className="mobile-brand">
            <div className="brand-mark small">N</div>
            <span>NoteSpace</span>
          </div>

          <div className="auth-header">
            <span className="eyebrow">Welcome back</span>
            <h2>Sign in to NoteSpace</h2>
            <p>Access your workspaces and continue where you left off.</p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email address</label>

              <input
                id="email"
                name="email"
                type="email"
                placeholder="name@example.com"
                value={formData.email}
                onChange={handleChange}
                autoComplete="email"
                required
              />
            </div>

            <div className="form-group">
              <div className="password-label-row">
                <label htmlFor="password">Password</label>
                <button type="button" className="text-button">
                  Forgot password?
                </button>
              </div>

              <input
                id="password"
                name="password"
                type="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                autoComplete="current-password"
                minLength={8}
                required
              />
            </div>

            <div className="form-options">
              <label className="remember-option">
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
            </div>

            <button
              type="submit"
              className="primary-auth-button"
              disabled={submitting}
            >
              {submitting ? "Signing in..." : "Sign in"}
            </button>
          </form>

          <div className="auth-divider">
            <span />
            <p>New to NoteSpace?</p>
            <span />
          </div>

          <Link to="/register" className="secondary-auth-button">
            Create an account
          </Link>

          <p className="auth-legal">
            By continuing, you agree to the NoteSpace Terms of Service and
            Privacy Policy.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Login;
