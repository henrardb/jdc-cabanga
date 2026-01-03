from typing import Iterable
from jdccabanga.models import Lesson
from html import escape

def generate_html_table(entries: Iterable[Lesson]) -> str:
    rows = []
    for item in entries:
        rows.append(
            f"""
                <tr>
                    <td>{escape(item.date or "")}</td>
                    <td>{escape(item.lessonName or "")}</td>
                    <td>{escape(item.lessonSubject or "")}</td>
                    <td>{escape(item.homework or "")}</td>
                </tr>
            """
        )

    body = f"""
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th style="border: 1px solid #ccc; padding: 4px; text-align:left;">Date</th>
                    <th style="border: 1px solid #ccc; padding: 4px; text-align:left;">Cours</th>
                    <th style="border: 1px solid #ccc; padding: 4px; text-align:left;">Sujet</th>
                    <th style="border: 1px solid #ccc; padding: 4px; text-align:left;">Devoir</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    """

    html = f"""
        <!DOCTYPE html>
        <head>
            <meta charset="utf-8" />
            <title>JDC Cabanga: Résumé des devoirs</title>
        </head>
        <html>
            <body>
                {body}
            </body>
        </html>
    """

    return html