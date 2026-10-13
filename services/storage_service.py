"""
Storage and Background Job Registry Service.
Provides thread-safe job tracking, SQLite/file persistence, and artifact management.
"""

import json
import sqlite3
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from config import settings
from models.job_models import VideoProcessingJob, JobStatus, JobArtifact
from utils.logging_config import logger

class StorageService:
    def __init__(self):
        self.lock = threading.Lock()
        self.jobs: Dict[str, VideoProcessingJob] = {}
        self.db_path = settings.data_dir / "studio.db"
        self._init_db()

    def _init_db(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT,
                    stage TEXT,
                    progress_pct REAL,
                    data_json TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()
            conn.close()

    def create_job(self, job_id: str, source_video_path: str = "", settings_dict: Optional[Dict[str, Any]] = None) -> VideoProcessingJob:
        job = VideoProcessingJob(
            job_id=job_id,
            source_video_path=source_video_path,
            settings=settings_dict or {}
        )
        job.log_stage("Job initialized and queued", 0.0)
        with self.lock:
            self.jobs[job_id] = job
            self._save_to_db(job)
        return job

    def get_job(self, job_id: str) -> Optional[VideoProcessingJob]:
        with self.lock:
            if job_id in self.jobs:
                return self.jobs[job_id]
            # Try fetching from SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                job_data = json.loads(row[0])
                job = VideoProcessingJob(**job_data)
                self.jobs[job_id] = job
                return job
        return None

    def update_job_stage(self, job_id: str, stage: str, progress: float) -> None:
        with self.lock:
            job = self.jobs.get(job_id)
            if job:
                job.log_stage(stage, progress)
                self._save_to_db(job)

    def mark_completed(self, job_id: str) -> None:
        with self.lock:
            job = self.jobs.get(job_id)
            if job:
                job.status = JobStatus.COMPLETED
                job.log_stage("Processing completed successfully", 100.0)
                self._save_to_db(job)

    def mark_failed(self, job_id: str, error_msg: str) -> None:
        with self.lock:
            job = self.jobs.get(job_id)
            if job:
                job.status = JobStatus.FAILED
                job.error_message = error_msg
                job.log_stage(f"Failed: {error_msg}", job.progress_pct)
                self._save_to_db(job)

    def cancel_job(self, job_id: str) -> None:
        with self.lock:
            job = self.jobs.get(job_id)
            if job:
                job.is_cancelled = True
                job.status = JobStatus.CANCELLED
                job.log_stage("Job cancelled by user", job.progress_pct)
                self._save_to_db(job)

    def register_artifact(self, job_id: str, name: str, category: str, file_path: Path, mime_type: str = "application/octet-stream") -> None:
        if not file_path.exists():
            logger.warning(f"Attempted to register non-existent artifact file: {file_path}")
            return
            
        with self.lock:
            job = self.jobs.get(job_id)
            if job:
                artifact = JobArtifact(
                    name=name,
                    category=category,
                    file_path=str(file_path),
                    file_size_bytes=file_path.stat().st_size,
                    mime_type=mime_type
                )
                job.artifacts.append(artifact)
                self._save_to_db(job)

    def list_jobs(self) -> List[VideoProcessingJob]:
        with self.lock:
            return list(self.jobs.values())

    def _save_to_db(self, job: VideoProcessingJob) -> None:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO jobs (job_id, status, stage, progress_pct, data_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job.job_id,
                job.status.value,
                job.stage,
                job.progress_pct,
                job.model_dump_json(),
                job.created_at,
                job.updated_at
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to persist job {job.job_id} to DB: {e}")

storage_service = StorageService()
