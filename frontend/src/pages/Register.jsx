import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { useAuth } from "../context/AuthContext";
import "./Auth.css";

function Register() {
  const navigate = useNavigate();

  const { register, isAuthenticated } = useAuth();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
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

    const cleanedName = formData.name.trim();

    const cleanedEmail = formData.email.trim();

    if (cleanedName.length < 2) {
      toast.error("Please enter your full name");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (formData.password.length < 8) {
      toast.error("Password must be at least 8 characters");
      return;
    }

    setSubmitting(true);

    try {
      await register(cleanedName, cleanedEmail, formData.password);

      toast.success("Account created successfully. Please sign in.");

      navigate("/login");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to create account");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-shell">
      <section className="auth-showcase">
        <div className="brand-mark">N</div>

        <div className="showcase-content">
          <span className="showcase-badge">Build your knowledge system</span>

          <h1>
            One workspace.
            <br />
            Everything organized.
          </h1>

          <p>
            Create structured workspaces for notes, projects, research,
            documentation, and shared knowledge.
          </p>

          <div className="showcase-points">
            <div>
              <span>01</span>

              <p>Create structured workspaces</p>
            </div>

            <div>
              <span>02</span>

              <p>Build nested knowledge pages</p>
            </div>

            <div>
              <span>03</span>

              <p>Track changes with version history</p>
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
            <span className="eyebrow">Get started</span>

            <h2>Create your NoteSpace account</h2>

            <p>
              Start organizing your work, ideas, and shared knowledge in one
              place.
            </p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Full name</label>

              <input
                id="name"
                name="name"
                type="text"
                placeholder="Your full name"
                value={formData.name}
                onChange={handleChange}
                autoComplete="name"
                minLength={2}
                maxLength={120}
                required
              />
            </div>

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
              <label htmlFor="password">Password</label>

              <input
                id="password"
                name="password"
                type="password"
                placeholder="Minimum 8 characters"
                value={formData.password}
                onChange={handleChange}
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm password</label>

              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                placeholder="Enter your password again"
                value={formData.confirmPassword}
                onChange={handleChange}
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                required
              />
            </div>

            <button
              type="submit"
              className="primary-auth-button"
              disabled={submitting}
            >
              {submitting ? "Creating account..." : "Create account"}
            </button>
          </form>

          <div className="auth-divider">
            <span />

            <p>Already using NoteSpace?</p>

            <span />
          </div>

          <Link to="/login" className="secondary-auth-button">
            Sign in
          </Link>

          <p className="auth-legal">
            By creating an account, you agree to the NoteSpace Terms of Service
            and Privacy Policy.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Register;
