"""Streamlit-based interactive test builder for mathpaper."""
from __future__ import annotations

import tempfile
from pathlib import Path

_PROBLEMS_DEFAULT = Path.cwd() / "problems"


def _render_preview_pdf(defn) -> bytes | None:
    """Build a single-problem PDF and return the raw bytes."""
    try:
        from mathpaper import Test

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preview"
            test = Test(title="Preview", course="")
            test.add(defn.build())
            test.build(str(out))
            pdf_path = out / "main.pdf"
            if pdf_path.exists():
                return pdf_path.read_bytes()
    except Exception as e:
        return None
    return None


def _pdf_to_image_bytes(pdf_bytes: bytes) -> bytes | None:
    """Convert first page of PDF to PNG bytes via PyMuPDF."""
    try:
        import fitz

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc.load_page(0)
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale for crisp rendering
        pix = page.get_pixmap(matrix=mat)
        return pix.tobytes("png")
    except ImportError:
        return None
    except Exception:
        return None


def main(problems_path: str | None = None) -> None:
    """Launch the Streamlit test builder. Called by `mathpaper explore`."""
    import subprocess
    import sys

    app_path = Path(__file__)
    args = [sys.executable, "-m", "streamlit", "run", str(app_path)]
    if problems_path:
        args += ["--", problems_path]
    subprocess.run(args)


def _streamlit_app() -> None:
    import sys
    import streamlit as st
    from mathpaper.library import ProblemLibrary

    st.set_page_config(
        page_title="mathpaper test builder",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        /* ── background ── */
        .stApp { background-color: #faf8f4; }
        [data-testid="stSidebar"] { background-color: #f0ece6; }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] { background-color: #f0ece6; }

        /* ── squared corners everywhere ── */
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] > div > div,
        [data-testid="stExpander"],
        [data-testid="stExpanderDetails"],
        .stAlert,
        [data-testid="stFileUploader"],
        [data-testid="stForm"] {
            border-radius: 2px !important;
        }

        /* ── buttons: pastel blue, plain border ── */
        .stButton > button {
            background-color: #d6e8f5;
            border: 1px solid #aac6e0;
            color: #1e3a50;
            font-weight: normal;
        }
        .stButton > button:hover {
            background-color: #c2daf0;
            border-color: #8fb5d8;
        }

        /* primary button: pastel sage green */
        .stButton > button[data-testid="baseButton-primary"] {
            background-color: #c8dfc8;
            border: 1px solid #9abf9a;
            color: #1a3320;
        }
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background-color: #b5d4b5;
        }

        /* download button */
        .stDownloadButton > button {
            background-color: #e8dff5;
            border: 1px solid #c0a8e0;
            color: #2a1a50;
            border-radius: 2px !important;
        }

        /* ── expanders: off-white header, thin border, all states ── */
        [data-testid="stExpander"] {
            border: 1px solid #d8cfc4 !important;
            background-color: #ffffff;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary:hover,
        [data-testid="stExpander"] summary:focus,
        [data-testid="stExpander"] summary:active {
            background-color: #f5f0ea !important;
            color: #2a2218 !important;
        }
        [data-testid="stExpanderToggleIcon"] { color: #7a6a5a; }

        /* ── inputs & selects ── */
        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] > div > div {
            background-color: #ffffff;
            border: 1px solid #c8bfb4;
        }

        /* ── info/success/error boxes ── */
        [data-testid="stAlert"] { border-radius: 2px !important; }

        /* ── image fullscreen button ── */
        [data-testid="StyledFullScreenButton"],
        button[title="View fullscreen"] {
            background-color: #d6e8f5 !important;
            border: 1px solid #aac6e0 !important;
            border-radius: 2px !important;
            color: #1e3a50 !important;
        }
        [data-testid="StyledFullScreenButton"]:hover,
        button[title="View fullscreen"]:hover {
            background-color: #c2daf0 !important;
        }

        /* ── dividers: softer ── */
        hr { border-color: #d8cfc4; }

        /* ── inline code tags (used for topic/difficulty chips) ── */
        code {
            background-color: #e8e0d8 !important;
            color: #2a2218 !important;
            border-radius: 2px !important;
            padding: 1px 5px !important;
        }

        /* ── global text color ── */
        .stApp, .stApp * {
            color: #2a2218;
        }
        /* inputs need their own override */
        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] > div > div {
            color: #2a2218 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Determine problems path from CLI arg or default
    problems_path = Path(sys.argv[1]) if len(sys.argv) > 1 else _PROBLEMS_DEFAULT

    # ── Load library ─────────────────────────────────────────────────────────
    @st.cache_resource
    def load_library(path: str):
        return ProblemLibrary(path)

    if not problems_path.exists():
        st.error(f"Problems directory not found: `{problems_path}`")
        st.info("Run `mathpaper explore ./problems` pointing to your problems folder.")
        st.stop()

    lib = load_library(str(problems_path))

    # ── Session state ─────────────────────────────────────────────────────────
    if "test_items" not in st.session_state:
        st.session_state.test_items = []  # list of problem ids

    # ── Sidebar: search filters ───────────────────────────────────────────────
    with st.sidebar:
        st.title("mathpaper")
        st.caption("test builder")
        st.divider()

        topics = ["(all)"] + lib.topics()
        sel_topic = st.selectbox("Topic", topics)

        courses = ["(all)"] + lib.courses()
        sel_course = st.selectbox("Course", courses)

        difficulties = ["(all)", "easy", "medium", "hard"]
        sel_difficulty = st.selectbox("Difficulty", difficulties)

        keywords = st.text_input("Keywords", placeholder="e.g. implicit")

        st.divider()
        st.caption(f"{len(lib.all())} problems loaded")

    # ── Search ────────────────────────────────────────────────────────────────
    results = lib.search(
        topic=None if sel_topic == "(all)" else sel_topic,
        course=None if sel_course == "(all)" else sel_course,
        difficulty=None if sel_difficulty == "(all)" else sel_difficulty,
        keywords=keywords or None,
    )

    # ── Two-column layout: search results | current test ─────────────────────
    col_search, col_test = st.columns([2, 1], gap="large")

    with col_search:
        st.subheader(f"Problems ({len(results)} found)")

        if not results:
            st.info("No problems match the current filters.")
        else:
            for defn in results:
                with st.expander(
                    f"**{defn.id}** — {defn.description}  "
                    f"`{defn.difficulty}` · {defn.topic}",
                    expanded=False,
                ):
                    tag_str = "  ".join(f"`{t}`" for t in defn.tags)
                    st.markdown(tag_str)

                    pcol, bcol = st.columns([3, 1])
                    with bcol:
                        if st.button("+ Add to test", key=f"add_{defn.id}"):
                            if defn.id not in st.session_state.test_items:
                                st.session_state.test_items.append(defn.id)
                                st.toast(f"Added {defn.id}")
                            else:
                                st.toast(f"{defn.id} already in test")

                    with pcol:
                        if st.button("Preview PDF", key=f"prev_{defn.id}"):
                            with st.spinner("Rendering…"):
                                pdf_bytes = _render_preview_pdf(defn)
                            if pdf_bytes is None:
                                st.error("Preview failed — is typst installed?")
                            else:
                                img_bytes = _pdf_to_image_bytes(pdf_bytes)
                                if img_bytes:
                                    st.image(img_bytes, use_container_width=True)
                                else:
                                    st.download_button(
                                        "Download preview PDF",
                                        data=pdf_bytes,
                                        file_name=f"preview_{defn.id}.pdf",
                                        mime="application/pdf",
                                    )

    with col_test:
        st.subheader("Current test")

        items = st.session_state.test_items
        if not items:
            st.info("Add problems from the left panel.")
        else:
            to_remove = []
            for i, pid in enumerate(items):
                rc1, rc2, rc3 = st.columns([3, 1, 1])
                rc1.markdown(f"**{i + 1}.** {pid}")
                if rc2.button("↑", key=f"up_{i}", disabled=i == 0):
                    items[i - 1], items[i] = items[i], items[i - 1]
                    st.rerun()
                if rc3.button("✕", key=f"rm_{i}"):
                    to_remove.append(pid)
            for pid in to_remove:
                items.remove(pid)
                st.rerun()

        st.divider()
        title = st.text_input("Title", value="Quiz")
        course_name = st.text_input("Course", value="")
        version = st.text_input("Version", value="A")
        out_dir = st.text_input("Output folder", value="out/quiz")

        build_col, export_col = st.columns(2)

        with build_col:
            if st.button("Build PDF ▸", disabled=not items, type="primary"):
                with st.spinner("Building…"):
                    try:
                        from mathpaper import Test

                        test = Test(title=title, course=course_name, version=version)
                        for pid in items:
                            test.add(lib.get(pid).build())
                        test.build(out_dir)
                        st.success(f"Built to `{out_dir}/`")
                    except Exception as e:
                        st.error(f"Build failed: {e}")

        with export_col:
            if st.button("Export .py", disabled=not items):
                lines = [
                    "from mathpaper import Test",
                    "from mathpaper.library import ProblemLibrary",
                    "",
                    f'lib = ProblemLibrary("./problems")',
                    f'quiz = Test(title="{title}", course="{course_name}", version="{version}")',
                ]
                for pid in items:
                    lines.append(f'quiz.add(lib.get("{pid}").build())')
                lines += ["", f'quiz.build("{out_dir}")']
                script = "\n".join(lines)
                st.code(script, language="python")
                st.download_button(
                    "Download script",
                    data=script,
                    file_name="quiz.py",
                    mime="text/plain",
                )


# When run directly by streamlit (streamlit run app.py), execute the UI.
if __name__ == "__main__":
    _streamlit_app()
