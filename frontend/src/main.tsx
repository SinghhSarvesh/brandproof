import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ShieldCheck,
  LayoutDashboard,
  BookOpen,
  FileCheck2,
  BarChart3,
  Plus,
  ArrowRight,
  LogOut,
  Check,
  AlertTriangle,
  Upload,
  History,
  Search,
  MessageSquare,
  ChevronRight,
} from "lucide-react";
import "./style.css";
type Item = Record<string, any>;
const initial = {
  title: "",
  text: "",
  purpose: "",
  audience: "Customers",
  channel: "social",
  attachment_id: null as number | null,
  image_purpose: "informative",
  alt_text: "",
  ai_consent: false,
};
function App() {
  const [token, setToken] = useState(sessionStorage.getItem("bp-token") || "");
  const [me, setMe] = useState<Item | null>(null);
  const [page, setPage] = useState("Overview");
  const [submissions, setSubmissions] = useState<Item[]>([]);
  const [sources, setSources] = useState<Item[]>([]);
  const [insights, setInsights] = useState<Item>({
    categories: {},
    rules: {},
    rejected_findings: [],
  });
  const [detail, setDetail] = useState<Item | null>(null);
  const [draft, setDraft] = useState(initial);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [login, setLogin] = useState({ email: "", password: "" });
  const [note, setNote] = useState("");
  const [exception, setException] = useState("");
  const [search, setSearch] = useState("");
  const [isLogo, setIsLogo] = useState(false);
  const [audit, setAudit] = useState<Item[]>([]);
  const [source, setSource] = useState({
    title: "",
    kind: "fact",
    text: "",
    match: "",
    replacement: "",
    valid_from: "",
    valid_until: "",
    active: false,
    scope: "all",
    supersedes: null as number | null,
  });
  async function api(path: string, body?: any, method?: string) {
    const r = await fetch("/api" + path, {
      method: method || (body ? "POST" : "GET"),
      headers: {
        ...(body instanceof FormData
          ? {}
          : { "Content-Type": "application/json" }),
        ...(token ? { Authorization: "Bearer " + token } : {}),
      },
      body:
        body instanceof FormData
          ? body
          : body
            ? JSON.stringify(body)
            : undefined,
    });
    const data = await r.json();
    if (!r.ok) {
      if (r.status === 401 && path != "/login") {
        sessionStorage.removeItem("bp-token");
        setToken("");
        setMe(null);
      }
      throw Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail),
      );
    }
    return data;
  }
  async function act(fn: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await fn();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function refresh() {
    const [m, s, r, i] = await Promise.all([
      api("/me"),
      api("/submissions"),
      api("/sources"),
      api("/insights"),
    ]);
    setMe(m);
    setSubmissions(s);
    setSources(r);
    setInsights(i);
  }
  useEffect(() => {
    if (token) void act(refresh);
  }, [token]);
  async function open(id: number) {
    setDetail(await api("/submissions/" + id));
    setEditing(false);
    setPage("Review");
    setNote("");
    setException("");
  }
  const rev = detail?.revisions[0];
  const run = detail?.reviews.find((x: Item) => x.revision_id === rev?.id);
  function newDraft() {
    setDetail(null);
    setDraft(initial);
    setEditing(true);
    setPage("New review");
  }
  async function save() {
    let item;
    if (detail) {
      await api(`/submissions/${detail.id}/revisions`, draft);
      item = detail;
    } else item = await api("/submissions", draft);
    await refresh();
    await open(item.id);
    setNotice("Revision saved. Run its checks before requesting approval.");
  }
  const field = (key: keyof typeof initial, label: string, multi = false) => (
    <label>
      {label}
      {multi ? (
        <textarea
          value={String(draft[key] ?? "")}
          onChange={(e) => setDraft({ ...draft, [key]: e.target.value })}
          rows={key === "text" ? 9 : 2}
        />
      ) : (
        <input
          value={String(draft[key] ?? "")}
          onChange={(e) => setDraft({ ...draft, [key]: e.target.value })}
        />
      )}
    </label>
  );
  if (!me)
    return (
      <div className="login">
        <div className="login-story">
          <div className="brand">
            <ShieldCheck /> BrandProof<span>WORKSPACE</span>
          </div>
          <div>
            <div className="eyebrow">CREATE FREELY. PUBLISH CONFIDENTLY.</div>
            <h1>
              A second look.
              <br />A stronger brand.
            </h1>
            <p>
              Bring your guidelines, content and reviewers into one clear,
              accountable workflow.
            </p>
            <div className="story-rule">
              <Check /> Evidence behind every concern
            </div>
            <div className="story-rule">
              <Check /> Your intent, preserved
            </div>
            <div className="story-rule">
              <Check /> People make the final call
            </div>
          </div>
          <small>TECHCIRCUIT 2026 · TEAM RAKSHITA7050</small>
        </div>
        <div className="login-form">
          <ShieldCheck size={36} />
          <h2>Welcome to BrandProof</h2>
          <p>Sign in to your brand workspace.</p>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void act(async () => {
                const r = await api("/login", login);
                sessionStorage.setItem("bp-token", r.token);
                setToken(r.token);
              });
            }}
          >
            <label>
              Email
              <input
                type="email"
                required
                autoComplete="username"
                value={login.email}
                onChange={(e) => setLogin({ ...login, email: e.target.value })}
              />
            </label>
            <label>
              Password
              <input
                type="password"
                required
                autoComplete="current-password"
                value={login.password}
                onChange={(e) =>
                  setLogin({ ...login, password: e.target.value })
                }
              />
            </label>
            {error && (
              <div role="alert" className="alert">
                {error}
              </div>
            )}
            <button disabled={busy} className="primary">
              {busy ? "Signing in…" : "Open workspace"} <ArrowRight size={16} />
            </button>
          </form>
          <small>
            Demo accounts are created by your administrator. Use fictional
            content in this prototype.
          </small>
        </div>
      </div>
    );
  return (
    <div className="app">
      <aside>
        <div className="brand">
          <ShieldCheck /> BrandProof
        </div>
        <div className="workspace">
          <span className="avatar">N</span>
          <div>
            Northstar Studio<small>Synthetic demo brand</small>
          </div>
        </div>
        <div className="nav-label">WORKSPACE</div>
        <nav>
          {[
            [LayoutDashboard, "Overview"],
            [FileCheck2, "Content reviews"],
            [BookOpen, "Brand sources"],
            [BarChart3, "Insights"],
            [History, "Activity"],
          ].map(([Icon, label]) => {
            const I = Icon as typeof ShieldCheck;
            return (
              <button
                key={String(label)}
                className={page === label ? "selected" : ""}
                onClick={() => {
                  setPage(String(label));
                  setDetail(null);
                  setEditing(false);
                  if (label === "Activity")
                    void act(async () => setAudit(await api("/audit")));
                }}
              >
                <I size={18} />
                {String(label)}
                {label === "Content reviews" && (
                  <span className="count">{submissions.length}</span>
                )}
              </button>
            );
          })}
        </nav>
        <div className="sidebar-note">
          <ShieldCheck size={20} />
          <strong>Human judgment, always.</strong>
          <p>Suggestions guide the work. Authorised reviewers decide.</p>
        </div>
        <div className="user">
          <span className="avatar">{me.role[0].toUpperCase()}</span>
          <div>
            {me.role}
            <small>{me.email}</small>
          </div>
          <button
            title="Sign out"
            onClick={() =>
              void act(async () => {
                await api("/logout", {});
                sessionStorage.removeItem("bp-token");
                setToken("");
                setMe(null);
              })
            }
          >
            <LogOut size={17} />
          </button>
        </div>
      </aside>
      <main>
        <header>
          <div>
            Workspace <ChevronRight size={14} /> <strong>{page}</strong>
          </div>
          <span className="mode">
            <span />{" "}
            {me.review_mode === "ai" ? "AI-assisted review" : "Rules-only demo"}
          </span>
        </header>
        <div className="content">
          {error && (
            <div role="alert" className="alert">
              <AlertTriangle size={17} />
              {error}
            </div>
          )}
          {notice && (
            <div role="status" className="notice">
              {notice}
            </div>
          )}
          {busy && (
            <div role="status" className="busy">
              Working…
            </div>
          )}
          {!editing && !detail && (
            <div className="page-head">
              <div>
                <div className="eyebrow">YOUR BRAND, IN FOCUS</div>
                <h1>
                  {page === "Overview"
                    ? "Good content starts with clarity."
                    : page}
                </h1>
                <p>
                  {page === "Overview"
                    ? "A shared place to check the details and move your content forward."
                    : page === "Brand sources"
                      ? "The approved facts and rules behind every review."
                      : page === "Insights"
                        ? "Patterns from real review runs, including repeated findings across revisions."
                        : "Follow every draft from first check to final decision."}
                </p>
              </div>
              {me.role !== "reviewer" && (
                <button className="primary" onClick={newDraft}>
                  <Plus size={17} />
                  New review
                </button>
              )}
            </div>
          )}
          {page === "Overview" && !editing && (
            <>
              <div className="stats">
                {[
                  [
                    "Content submissions",
                    submissions.length,
                    "Across your workspace",
                  ],
                  [
                    "Awaiting review",
                    submissions.filter((x) => x.status === "awaiting_review")
                      .length,
                    "Ready for a human decision",
                  ],
                  [
                    "Approved content",
                    submissions.filter((x) => x.status === "approved").length,
                    "Exact revisions, recorded",
                  ],
                  [
                    "Active source rules",
                    sources.filter((x) => x.active).length,
                    "Check validity dates in sources",
                  ],
                ].map(([label, n, caption]) => (
                  <div className="stat" key={label}>
                    <span>{label}</span>
                    <strong>{n}</strong>
                    <small>{caption}</small>
                  </div>
                ))}
              </div>
              <div className="welcome">
                <div>
                  <div className="eyebrow">FROM DRAFT TO DECISION</div>
                  <h2>
                    Keep the creativity.
                    <br />
                    Catch the inconsistencies.
                  </h2>
                  <p>
                    Check claims against approved sources, make deliberate
                    changes and send the right revision for approval.
                  </p>
                  <button onClick={() => setPage("Brand sources")}>
                    Explore brand sources <ArrowRight size={16} />
                  </button>
                </div>
                <div className="workflow">
                  {[
                    "01 · Establish approved sources",
                    "02 · Review and refine content",
                    "03 · Record a human decision",
                  ].map((s, i) => (
                    <div key={s}>
                      <span className="step">
                        {i === 2 ? (
                          <ShieldCheck size={22} />
                        ) : (
                          <Check size={21} />
                        )}
                      </span>
                      {s}
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
          {["Overview", "Content reviews"].includes(page) && !editing && (
            <section className="panel">
              <div className="panel-head">
                <h2>
                  {page === "Overview"
                    ? "Recent content"
                    : "All content reviews"}
                </h2>
                <div className="search">
                  <Search size={15} />
                  <input
                    placeholder="Find content…"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                  />
                </div>
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>CONTENT</th>
                      <th>STATUS</th>
                      <th>REVISION ID</th>
                      <th />
                    </tr>
                  </thead>
                  <tbody>
                    {submissions
                      .filter((x) =>
                        x.title.toLowerCase().includes(search.toLowerCase()),
                      )
                      .map((x) => (
                        <tr key={x.id}>
                          <td>
                            <button
                              className="title-button"
                              onClick={() => void act(() => open(x.id))}
                            >
                              <span className="file-icon">
                                <FileCheck2 size={19} />
                              </span>
                              {x.title}
                            </button>
                          </td>
                          <td>
                            <span className={"badge " + x.status}>
                              {x.status.replaceAll("_", " ")}
                            </span>
                          </td>
                          <td>#{x.latest_revision}</td>
                          <td>
                            <button
                              aria-label={"Open " + x.title}
                              onClick={() => void act(() => open(x.id))}
                            >
                              <ArrowRight size={18} />
                            </button>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
              {!submissions.length && (
                <div className="empty">
                  <FileCheck2 />
                  <h3>Your first review starts here</h3>
                  <p>Add approved sources, then submit a draft to check.</p>
                  <button onClick={newDraft}>
                    Create a review <ArrowRight size={16} />
                  </button>
                </div>
              )}
            </section>
          )}
          {editing && (
            <>
              <div className="page-head">
                <div className="eyebrow">
                  CREATOR WORKSPACE
                  <h1>
                    {detail
                      ? "Create a new revision"
                      : "What are you working on?"}
                  </h1>
                  <p>
                    Give the reviewer your purpose, audience and the content to
                    check.
                  </p>
                </div>
              </div>
              <div className="panel form-panel">
                {field("title", "Content title")}
                <div className="two">
                  {field("purpose", "Campaign purpose")}
                  {field("audience", "Intended audience")}
                </div>
                <label>
                  Channel
                  <select
                    value={draft.channel}
                    onChange={(e) =>
                      setDraft({ ...draft, channel: e.target.value })
                    }
                  >
                    <option>social</option>
                    <option>email</option>
                    <option>website</option>
                  </select>
                </label>
                <label className="checkbox">
                  <input
                    type="checkbox"
                    checked={isLogo}
                    onChange={(e) => setIsLogo(e.target.checked)}
                  />
                  The next image upload is a standalone logo asset.
                </label>
                <label className="upload">
                  <Upload size={20} /> Import a text PDF or image (5 MB maximum)
                  <input
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file)
                        void act(async () => {
                          const f = new FormData();
                          f.append("file", file);
                          f.append("is_logo", String(isLogo));
                          const r = await api("/extract", f);
                          setDraft({
                            ...draft,
                            text: r.format === "pdf" ? r.text : draft.text,
                            attachment_id: r.id,
                          });
                          setNotice(
                            `Imported ${r.name}. ${r.format === "image" ? "OCR text will be checked against configured rules." : ""}`,
                          );
                        });
                    }}
                  />
                </label>
                {field("text", "Draft text", true)}
                {draft.attachment_id && (
                  <>
                    <label>
                      Image purpose
                      <select
                        value={draft.image_purpose}
                        onChange={(e) =>
                          setDraft({ ...draft, image_purpose: e.target.value })
                        }
                      >
                        <option>informative</option>
                        <option>functional</option>
                        <option>decorative</option>
                      </select>
                    </label>
                    {field("alt_text", "Proposed alt text")}
                  </>
                )}
                {me.review_mode === "ai" && (
                  <label className="checkbox">
                    <input
                      type="checkbox"
                      checked={draft.ai_consent}
                      onChange={(e) =>
                        setDraft({ ...draft, ai_consent: e.target.checked })
                      }
                    />
                    I consent to sending this draft, purpose, audience and
                    relevant approved sources to {me.ai_provider}. Use synthetic
                    data only until provider retention has been reviewed.
                  </label>
                )}
                <div className="actions">
                  <button
                    className="primary"
                    disabled={busy}
                    onClick={() => void act(save)}
                  >
                    Save revision <ArrowRight size={16} />
                  </button>
                  <button
                    onClick={() => {
                      setEditing(false);
                      setPage("Overview");
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </>
          )}
          {detail && !editing && (
            <>
              <div className="page-head">
                <div>
                  <div className="eyebrow">
                    CONTENT REVIEW · REVISION #{rev.id}
                  </div>
                  <h1>{rev.title}</h1>
                  <p>
                    {rev.purpose} · {rev.audience} · {rev.channel}
                  </p>
                </div>
                <span className={"badge " + detail.status}>
                  {detail.status.replaceAll("_", " ")}
                </span>
              </div>
              <div className="review-grid">
                <section className="panel">
                  <div className="panel-head">
                    <h2>The current draft</h2>
                    <FileCheck2 size={19} />
                  </div>
                  <div className="draft-text">{rev.text}</div>
                  <div className="inner">
                    <small>
                      Each saved edit creates a new revision. Approval never
                      carries over to changed content.
                    </small>
                    <div className="actions">
                      {me.role !== "reviewer" && (
                        <>
                          <button
                            disabled={busy}
                            className="primary"
                            onClick={() =>
                              void act(async () => {
                                await api(`/revisions/${rev.id}/review`, {});
                                await open(detail.id);
                                await refresh();
                              })
                            }
                          >
                            Run checks
                          </button>
                          <button
                            onClick={() => {
                              setDraft({ ...initial, ...rev });
                              setEditing(true);
                            }}
                          >
                            Edit revision
                          </button>
                          <button
                            disabled={busy}
                            onClick={() =>
                              void act(async () => {
                                await api(
                                  `/submissions/${detail.id}/request-approval`,
                                  { revision_id: rev.id },
                                );
                                await open(detail.id);
                                await refresh();
                              })
                            }
                          >
                            Request approval
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                  <div className="inner border-top">
                    <h3>
                      <MessageSquare size={17} /> Discussion & decision
                    </h3>
                    {detail.comments.map((x: Item) => (
                      <div className="comment" key={x.id}>
                        <strong>{x.author}</strong>
                        <p>{x.text}</p>
                      </div>
                    ))}
                    <label>
                      Comment or decision reason
                      <textarea
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        rows={3}
                      />
                    </label>
                    <button
                      disabled={busy || !note.trim()}
                      onClick={() =>
                        void act(async () => {
                          await api("/comments", {
                            revision_id: rev.id,
                            text: note,
                          });
                          await open(detail.id);
                        })
                      }
                    >
                      Add comment
                    </button>
                    {me.role !== "creator" && (
                      <>
                        <label>
                          Exception reason (required for unresolved
                          high-severity findings)
                          <textarea
                            value={exception}
                            onChange={(e) => setException(e.target.value)}
                            rows={2}
                          />
                        </label>
                        <div className="actions">
                          {["approved", "changes_requested"].map((action) => (
                            <button
                              key={action}
                              disabled={busy || !note.trim()}
                              className={action === "approved" ? "primary" : ""}
                              onClick={() =>
                                void act(async () => {
                                  await api(
                                    `/submissions/${detail.id}/approve`,
                                    {
                                      revision_id: rev.id,
                                      action,
                                      reason: note,
                                      exception_reason: exception,
                                    },
                                  );
                                  await open(detail.id);
                                  await refresh();
                                })
                              }
                            >
                              {action === "approved"
                                ? "Approve revision"
                                : "Request changes"}
                            </button>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                </section>
                <section>
                  <div className="panel">
                    <div className="panel-head">
                      <h2>Review findings</h2>
                      <span className="count">
                        {run?.findings.length ?? "—"}
                      </span>
                    </div>
                    {run ? (
                      <>
                        <div className="inner">
                          <span
                            className={
                              "badge " +
                              (run.status === "complete"
                                ? "approved"
                                : "changes_requested")
                            }
                          >
                            {run.status === "complete"
                              ? "Checks complete"
                              : "Review incomplete"}
                          </span>
                          <p className="muted">
                            {run.mode === "rules_only"
                              ? "Limited review: configured rules only. Semantic tone and paraphrased claims were not checked."
                              : "AI-assisted review with verified source references. Human judgment is still required."}
                          </p>
                          {run.error && <p className="alert">{run.error}</p>}
                        </div>
                        {run.findings.map((f: Item) => (
                          <article className="finding" key={f.index}>
                            <div className="finding-top">
                              <span className={"severity " + f.severity}>
                                {f.severity}
                              </span>
                              <span>{f.category.replaceAll("_", " ")}</span>
                            </div>
                            <blockquote>{f.quote}</blockquote>
                            <p>{f.explanation}</p>
                            <details>
                              <summary>
                                <BookOpen size={14} /> {f.source_title} · v
                                {f.source_version}
                              </summary>
                              <p>{f.evidence}</p>
                              {f.source_id && (
                                <small>Source #{f.source_id}</small>
                              )}
                            </details>
                            {f.suggestion && (
                              <div className="suggestion">
                                <small>SUGGESTED CORRECTION</small>
                                <p>{f.suggestion}</p>
                              </div>
                            )}
                            {me.role !== "reviewer" && (
                              <div className="actions">
                                <button
                                  onClick={() => {
                                    setDraft({ ...initial, ...rev });
                                    setEditing(true);
                                    setNotice(
                                      "Edit the relevant passage using the suggestion, then save a new revision.",
                                    );
                                  }}
                                >
                                  Edit with suggestion
                                </button>
                                <button
                                  onClick={() => {
                                    const reason = window.prompt(
                                      "Why are you rejecting this finding?",
                                    );
                                    if (reason?.trim())
                                      void act(async () => {
                                        await api("/decisions", {
                                          review_id: run.id,
                                          index: f.index,
                                          action: "rejected",
                                          reason,
                                        });
                                        setNotice(
                                          "Rejection recorded. High-severity findings still need a reviewer exception.",
                                        );
                                        await refresh();
                                      });
                                  }}
                                >
                                  Reject finding
                                </button>
                              </div>
                            )}
                          </article>
                        ))}
                        {!run.findings.length && (
                          <div className="empty">
                            <ShieldCheck />
                            <h3>No findings in completed checks</h3>
                            <p>
                              This is not a guarantee of factual accuracy or
                              brand compliance.
                            </p>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="empty">
                        <Search />
                        <h3>Ready for a closer look</h3>
                        <p>
                          Run checks to compare this draft with approved brand
                          sources.
                        </p>
                      </div>
                    )}
                  </div>
                  <div className="panel timeline">
                    <h3>Revision history</h3>
                    {detail.revisions.map((r: Item) => (
                      <details key={r.id}>
                        <summary>
                          Revision #{r.id} ·{" "}
                          {new Date(r.created_at * 1000).toLocaleString()}
                        </summary>
                        <p className="draft-text">{r.text}</p>
                      </details>
                    ))}
                    {detail.approvals.map((a: Item) => (
                      <p key={a.id}>
                        <strong>
                          {a.action.replaceAll("_", " ")} · #{a.revision_id}
                        </strong>
                        <br />
                        {a.reviewer}: {a.reason}
                        {a.exception_reason && (
                          <>
                            <br />
                            Exception: {a.exception_reason}
                          </>
                        )}
                      </p>
                    ))}
                  </div>
                </section>
              </div>
            </>
          )}
          {page === "Brand sources" && !editing && (
            <div className="review-grid">
              <section className="panel">
                <div className="panel-head">
                  <h2>Source of truth</h2>
                  <span className="count">{sources.length}</span>
                </div>
                {sources.map((x) => (
                  <article className="source" key={x.id}>
                    <div className="finding-top">
                      <span className="badge">{x.kind}</span>
                      <small>
                        #{x.id} · v{x.version} ·{" "}
                        {x.active ? "Confirmed" : "Inactive"}
                      </small>
                    </div>
                    <h3>{x.title}</h3>
                    <p>{x.text}</p>
                    <small>
                      Scope: {x.scope} · Valid until:{" "}
                      {x.valid_until || "No expiry"}
                    </small>
                    {me.role === "manager" && (
                      <button
                        onClick={() =>
                          setSource({
                            ...source,
                            ...x,
                            supersedes: x.id,
                            active: true,
                          })
                        }
                      >
                        Create replacement version <ArrowRight size={14} />
                      </button>
                    )}
                  </article>
                ))}
                {!sources.length && (
                  <div className="empty">
                    Add the first approved rule to begin.
                  </div>
                )}
              </section>
              {me.role === "manager" ? (
                <section className="panel form-panel">
                  <h2>
                    {source.supersedes
                      ? "Replace source #" + source.supersedes
                      : "Add a brand source"}
                  </h2>
                  <p className="muted">
                    Review and confirm each rule before it can influence content
                    checks.
                  </p>
                  <label>
                    Import guideline PDF text
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file)
                          void act(async () => {
                            const data = new FormData();
                            data.append("file", file);
                            const r = await api("/extract", data);
                            setSource({
                              ...source,
                              title: file.name,
                              text: r.text,
                              active: false,
                            });
                            setNotice(
                              "Extracted candidate text. Select one rule, configure its match and confirm it before saving.",
                            );
                          });
                      }}
                    />
                  </label>
                  {(
                    [
                      "title",
                      "text",
                      "match",
                      "replacement",
                      "scope",
                      "valid_from",
                      "valid_until",
                    ] as const
                  ).map((key) => (
                    <label key={key}>
                      {
                        {
                          title: "Source title",
                          text: "Approved statement or rule",
                          match: "Match phrase / WIDTHxHEIGHT / logo SHA-256",
                          replacement: "Suggested replacement",
                          scope: "Scope (all, social, email, website)",
                          valid_from: "Valid from",
                          valid_until: "Valid until",
                        }[key]
                      }
                      {key === "text" ? (
                        <textarea
                          value={source[key]}
                          onChange={(e) =>
                            setSource({ ...source, [key]: e.target.value })
                          }
                        />
                      ) : (
                        <input
                          type={key.startsWith("valid") ? "date" : "text"}
                          value={source[key]}
                          onChange={(e) =>
                            setSource({ ...source, [key]: e.target.value })
                          }
                        />
                      )}
                    </label>
                  ))}
                  <label>
                    Rule type
                    <select
                      value={source.kind}
                      onChange={(e) =>
                        setSource({ ...source, kind: e.target.value })
                      }
                    >
                      {[
                        "fact",
                        "term",
                        "tone",
                        "claim",
                        "dimension",
                        "logo",
                      ].map((x) => (
                        <option key={x}>{x}</option>
                      ))}
                    </select>
                  </label>
                  <label className="checkbox">
                    <input
                      type="checkbox"
                      checked={source.active}
                      onChange={(e) =>
                        setSource({ ...source, active: e.target.checked })
                      }
                    />
                    I have verified this source and approve it for use.
                  </label>
                  <button
                    className="primary"
                    disabled={busy}
                    onClick={() =>
                      void act(async () => {
                        await api("/sources", source);
                        await refresh();
                        setNotice(
                          "Source version saved. Existing approvals may require revalidation.",
                        );
                        setSource({
                          ...source,
                          title: "",
                          text: "",
                          match: "",
                          replacement: "",
                          active: false,
                          supersedes: null,
                        });
                      })
                    }
                  >
                    Save source
                  </button>
                </section>
              ) : (
                <div className="panel form-panel">
                  <BookOpen />
                  <h2>Managed, approved, traceable.</h2>
                  <p>
                    Your brand manager maintains these source versions. Every
                    finding links back to the version used.
                  </p>
                </div>
              )}
            </div>
          )}
          {page === "Insights" && (
            <div className="review-grid">
              <section className="panel form-panel">
                <h2>Recurring issue categories</h2>
                <p className="muted">
                  Counts include repeated findings across review runs; they are
                  not unique defect counts.
                </p>
                {Object.entries(insights.categories).map(([k, v]) => (
                  <div className="bar-row" key={k}>
                    <div>
                      {k.replaceAll("_", " ")}
                      <strong>{String(v)}</strong>
                    </div>
                    <div className="bar">
                      <i
                        style={{
                          width: `${Math.min(100, (Number(v) / Math.max(1, ...Object.values(insights.categories).map(Number))) * 100)}%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
                {!Object.keys(insights.categories).length && (
                  <p>No review findings yet.</p>
                )}
              </section>
              <section className="panel form-panel">
                <h2>Rules that may need clarification</h2>
                <p className="muted">
                  Rejected findings are signals for a manager to inspect, not
                  automatic guideline changes.
                </p>
                {insights.rejected_findings.map((x: Item) => (
                  <div className="comment" key={x.id}>
                    <strong>
                      Review #{x.review_id} · finding {x.index + 1}
                    </strong>
                    <p>{x.reason}</p>
                    <small>{x.author}</small>
                  </div>
                ))}
                {!insights.rejected_findings.length && (
                  <p>No disputed findings recorded.</p>
                )}
              </section>
            </div>
          )}
          {page === "Activity" && (
            <section className="panel form-panel">
              <h2>Recorded workspace activity</h2>
              {audit.map((x) => (
                <div className="activity" key={x.id}>
                  <History size={17} />
                  <div>
                    <strong>{x.action.replaceAll("_", " ")}</strong>
                    <small>
                      {x.actor} · record #{x.target}
                    </small>
                  </div>
                  <time>{new Date(x.at * 1000).toLocaleString()}</time>
                </div>
              ))}
            </section>
          )}
          <footer>
            BrandProof · Evidence-led review, human-led decisions.
            <span>Prototype · Synthetic materials only</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
