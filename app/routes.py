import os
from datetime import datetime
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import select, desc

from .db import SessionLocal
from .models import Base, LogEntry
from .openai_client import transcribe_audio, formalize_text

bp = Blueprint("main", __name__)

ALLOWED_EXTS = {"mp3", "m4a", "wav", "aac", "flac", "ogg", "webm"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


@bp.route("/")
def index():
    return redirect(url_for("main.upload"))


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "audio" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        f = request.files["audio"]
        if f.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)
        if not allowed_file(f.filename):
            flash("Unsupported file type", "error")
            return redirect(request.url)

        filename = secure_filename(f.filename)
        upload_dir = current_app.config["UPLOAD_DIR"]
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}_{filename}")
        f.save(path)

        # Transcribe → Formalize → Store
        try:
            raw_text, duration = transcribe_audio(path)
            formal = formalize_text(raw_text)

            with SessionLocal() as db:
                entry = LogEntry(
                    filename=os.path.basename(path),
                    transcript_raw=raw_text,
                    transcript_formal=formal,
                    duration_sec=duration,
                )
                db.add(entry)
                db.commit()
                flash("Uploaded and processed successfully.", "success")
                return redirect(url_for("main.logs"))
        except Exception as e:
            current_app.logger.exception("Processing failed")
            flash(f"Processing failed: {e}", "error")
            return redirect(request.url)

    return render_template("upload.html")


@bp.route("/logs")
def logs():
    page = max(int(request.args.get("page", 1)), 1)
    page_size = 20
    offset = (page - 1) * page_size

    with SessionLocal() as db:
        stmt = select(LogEntry).order_by(desc(LogEntry.created_at)).offset(offset).limit(page_size)
        entries = db.execute(stmt).scalars().all()
    return render_template("logs.html", entries=entries, page=page, page_size=page_size)


@bp.route("/uploads/<path:fname>")
def uploaded_file(fname):
    return send_from_directory(current_app.config["UPLOAD_DIR"], fname, as_attachment=True)
