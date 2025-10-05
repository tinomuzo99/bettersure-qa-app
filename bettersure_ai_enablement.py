
# ==========================================
# File: bettersure_ai_enablement.py
# ==========================================
from __future__ import annotations
import os
import argparse
from dataclasses import dataclass
from typing import List
import re
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer, SimpleDocTemplate, PageBreak
from reportlab.lib.enums import TA_LEFT

# Load .env if present
load_dotenv()

QUESTIONS: List[str] = [
    "What is life insurance, and how does it work?",
    "What’s the difference between life, health, and short-term insurance?",
    "How do insurers decide how much premium I should pay?",
    "Why do premiums increase as I get older?",
    "What does ‘excess’ mean in household insurance?",
    "What does a household insurance policy cover?",
    "How do I know if I need critical illness or disability cover?",
    "What is a beneficiary, and why do I need to nominate one?",
    "What is underwriting in insurance?",
    "What is risk pooling, and why is it important for insurance?",
    "How do insurers use mortality tables?",
    "What is adverse selection in insurance?",
    "What is the principle of indemnity?",
    "What is reinsurance, and why do insurers use it?",
    "What is moral hazard, and how do insurers reduce it?",
    "What’s the difference between short-term and long-term insurance?",
    "How are claims usually processed, step by step?",
    "What can cause a claim to be rejected?",
    "How do insurers detect fraud in claims?",
    "How could AI improve the way insurers handle clients and claims?",
]

@dataclass
class AIClient:
    model: str = "gpt-4o-mini"

    def __post_init__(self):
        self.client = OpenAI()

    def ask(self, question: str) -> str:
        system_prompt = (
            "You are a helpful South African insurance guide. Use plain, friendly "
            "language for consumers. Keep answers concise (80–120 words). Avoid "
            "jargon. If a term is essential, define it simply. Do not give legal "
            "advice; include a short, practical tip when helpful."
        )
        user_prompt = f"Question: {question}\nAnswer:"

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()


def write_csv(pairs: List[tuple[str, str]], out_path: str = "answers.csv") -> str:
    df = pd.DataFrame(pairs, columns=["question", "answer"])
    df.to_csv(out_path, index=False)
    return out_path


def draw_header(c: canvas.Canvas, title: str, primary: colors.Color, accent: colors.Color):
    width, height = A4
    c.setFillColor(primary)
    c.rect(0, height - 22 * mm, width, 22 * mm, fill=1, stroke=0)
    c.setFillColor(accent)
    c.rect(0, height - 23.5 * mm, width, 1.5 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(15 * mm, height - 15 * mm, title)


def export_pdf(pairs: List[tuple[str, str]], out_path: str = "answers.pdf") -> str:
    """Robust, auto-paginating PDF export using SimpleDocTemplate.
    Prints progress per page and avoids infinite pagination loops.
    """
    primary = colors.HexColor("#214B61")
    accent = colors.HexColor("#F58220")

    width, height = A4

    # Styles
    style_q = ParagraphStyle(
        name="Q",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=primary,
        alignment=TA_LEFT,
        spaceAfter=2 * mm,
    )
    style_a = ParagraphStyle(
        name="A",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=6 * mm,
    )
    style_footer = ParagraphStyle(
        name="Footer",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=4 * mm,
    )

    # Build story
    story = [Spacer(1, 6 * mm)]
    for i, (q, a) in enumerate(pairs, start=1):
        story.append(Paragraph(f"{i}. {q}", style_q))
        # Convert markdown bold (**text**) and italics (*text*) to HTML tags
        ans_html = a
        ans_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', ans_html)
        ans_html = re.sub(r'\*(.+?)\*', r'<i>\1</i>', ans_html)
        ans_html = ans_html.replace("\n", "<br/>")
        story.append(Paragraph(ans_html, style_a))
        story.append(Spacer(1, 2 * mm))

    # Optional back cover content
    story.append(PageBreak())
    story.append(Paragraph("Answers generated by an AI assistant using OpenAI.", style_footer))
    story.append(Paragraph("Content is general information and not financial advice.", style_footer))

    # Use SimpleDocTemplate for reliable pagination
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=40 * mm,   # leave space for the header bar
        bottomMargin=15 * mm,
    )

    def on_page(c: canvas.Canvas, _doc):
        # Progress printout and header drawing for each page
        print(f"Adding content to PDF page {c.getPageNumber()}…")
        draw_header(c, "BetterSure – Insurance Q&A", primary, accent)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path


def run_batch(model: str, make_pdf: bool) -> None:
    ai = AIClient(model=model)
    qa_pairs: List[tuple[str, str]] = []
    for idx, q in enumerate(QUESTIONS, start=1):
        print(f"Answering Q{idx}/{len(QUESTIONS)}: {q}")
        a = ai.ask(q)
        qa_pairs.append((q, a))

    csv_path = write_csv(qa_pairs, out_path="answers.csv")
    print(f"Saved CSV -> {csv_path}")

    if make_pdf:
        pdf_path = export_pdf(qa_pairs, out_path="answers.pdf")
        print(f"Saved PDF -> {pdf_path}")


def run_single(model: str, question: str) -> None:
    ai = AIClient(model=model)
    print(ai.ask(question))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BetterSure Coding Exercise – batch Q&A")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model (default: gpt-4o-mini)")
    parser.add_argument("--make-pdf", action="store_true", help="Also export answers.pdf with BetterSure brand colours")
    parser.add_argument("--single", default=None, help="Ask one ad-hoc question instead of the batch")
    args = parser.parse_args()

    if args.single:
        run_single(args.model, args.single)
    else:
        run_batch(args.model, args.make_pdf)
