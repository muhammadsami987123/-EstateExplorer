from typing import Dict, Any, Optional
import io
import uuid
from datetime import datetime
from app.json_db import JsonDB
from app.services.matching import score_property

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

async def generate_report(preferences: Dict[str, Any]) -> Dict[str, Any]:
    all_properties = JsonDB.load('properties')
    intent = preferences.get('intent', 'buy').lower()
    target_listing_type = 'rent' if intent == 'rent' else 'sale'

    # Filter relevant properties
    relevant = [p for p in all_properties if p.get('listing_type') == target_listing_type and p.get('status', 'active') == 'active']
    if not relevant:
        relevant = [p for p in all_properties if p.get('status', 'active') == 'active']

    # Filter by country if provided
    country = preferences.get('country')
    if country:
        country_props = [p for p in relevant if p.get('country', '').lower() == country.lower()]
        if country_props:
            relevant = country_props

    # Score all
    scored = []
    for prop in relevant:
        match = score_property(prop, preferences)
        scored.append({**prop, 'match_score': match['score'], 'match_data': match})
    scored.sort(key=lambda x: x['match_score'], reverse=True)

    # Get market snapshot
    city = preferences.get('city', '')
    market_snapshot = None
    if city:
        market_data = JsonDB.load('market_data')
        market_snapshot = next(
            (m for m in market_data if city.lower() in m.get('city', '').lower() or city.lower() in m.get('location_name', '').lower()),
            None
        )
    if not market_snapshot:
        market_snapshot = JsonDB.load('market_data')[0] if JsonDB.load('market_data') else None

    total_strong = len([s for s in scored if s.get('match_score', 0) >= 60])

    report = {
        'id': str(uuid.uuid4()),
        'created_at': datetime.utcnow().isoformat() + "Z",
        'preferences': preferences,
        'recommended_properties': scored[:5],
        'alternative_properties': scored[5:10],
        'market_snapshot': market_snapshot,
        'total_matches': total_strong or len(scored[:5]),
        'data_type': 'Demo Dataset',
        'next_steps': [
            'Shortlist 3-5 properties that best fit your requirements',
            'Schedule property viewings for your top picks',
            'Verify ownership documents and legal status with relevant authority',
            'Confirm current property condition in person with an independent surveyor',
            'Review all applicable taxes, transfer charges, and registry fees',
            'Compare final offers and negotiate closing terms before signing',
        ],
        'disclaimer': 'All data shown in this report is from a demonstration dataset and should not be used for actual investment or purchase decisions.'
    }

    # Save report
    JsonDB.insert('reports', report)
    return report

def generate_pdf(report: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        fontName='Helvetica'
    )
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )
    bold_body_style = ParagraphStyle(
        'BoldBodyTextCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold'
    )
    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#94A3B8'),
        fontName='Helvetica-Oblique'
    )

    story = []

    # Title & Header
    story.append(Paragraph("AI Real Estate Explorer", title_style))
    story.append(Paragraph(f"Personalized Property & Market Intelligence Report — Generated {report.get('created_at', '')[:10]}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    # Preferences Summary
    prefs = report.get('preferences', {})
    story.append(Paragraph("Search Criteria & User Parameters", h2_style))
    pref_data = [
        [
            Paragraph("<b>Intent:</b> " + str(prefs.get('intent', 'Buy')).title(), body_style),
            Paragraph("<b>Property Type:</b> " + str(prefs.get('property_type', 'Any')).title(), body_style),
        ],
        [
            Paragraph("<b>Location:</b> " + f"{prefs.get('area', '')} {prefs.get('city', '')}".strip() or "All Areas", body_style),
            Paragraph(f"<b>Max Budget:</b> {prefs.get('currency', 'PKR')} {prefs.get('max_budget', 0):,.0f}" if prefs.get('max_budget') else "<b>Budget:</b> Flexible", body_style),
        ],
        [
            Paragraph("<b>Bedrooms:</b> " + str(prefs.get('bedrooms') or "Flexible"), body_style),
            Paragraph("<b>Total Matches Found:</b> " + str(report.get('total_matches', 0)), body_style),
        ]
    ]
    pref_table = Table(pref_data, colWidths=[260, 260])
    pref_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(pref_table)
    story.append(Spacer(1, 14))

    # Recommended Properties
    story.append(Paragraph("Top Recommended Properties", h2_style))
    recs = report.get('recommended_properties', [])
    if recs:
        table_rows = [
            [
                Paragraph("<b>Property Details</b>", bold_body_style),
                Paragraph("<b>Location</b>", bold_body_style),
                Paragraph("<b>Price</b>", bold_body_style),
                Paragraph("<b>Beds/Baths</b>", bold_body_style),
                Paragraph("<b>Match Score</b>", bold_body_style),
            ]
        ]
        for p in recs:
            match_score = f"{p.get('match_score', 0)}%"
            table_rows.append([
                Paragraph(f"<b>{p.get('title', '')}</b><br/><font color='#64748B'>{p.get('type', '').title()} • {p.get('covered_area_sqft', 0):,} sqft</font>", body_style),
                Paragraph(f"{p.get('area', '')}, {p.get('city', '')}", body_style),
                Paragraph(f"{p.get('currency', 'PKR')} {p.get('price', 0):,.0f}", bold_body_style),
                Paragraph(f"{p.get('bedrooms', 0)} Bed / {p.get('bathrooms', 0)} Bath", body_style),
                Paragraph(f"<font color='#059669'><b>{match_score}</b></font>", bold_body_style),
            ])
        prop_table = Table(table_rows, colWidths=[180, 110, 95, 75, 60])
        prop_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('PADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(prop_table)
    else:
        story.append(Paragraph("No direct property matches found for this specific criteria.", body_style))

    story.append(Spacer(1, 14))

    # Market Snapshot
    mkt = report.get('market_snapshot')
    if mkt:
        story.append(Paragraph(f"Market Overview — {mkt.get('location_name', 'Target Market')}", h2_style))
        mkt_rows = [
            [
                Paragraph(f"<b>Avg Sale Price:</b> {mkt.get('currency', 'PKR')} {mkt.get('avg_price_sale', 0):,.0f}", body_style),
                Paragraph(f"<b>Median Sale Price:</b> {mkt.get('currency', 'PKR')} {mkt.get('median_price_sale', 0):,.0f}", body_style),
            ],
            [
                Paragraph(f"<b>Price per Sqft:</b> {mkt.get('currency', 'PKR')} {mkt.get('price_per_sqft_sale', 0):,.0f}", body_style),
                Paragraph(f"<b>Market Demand Score:</b> {mkt.get('demand_score', 0)}/100", body_style),
            ]
        ]
        mkt_table = Table(mkt_rows, colWidths=[260, 260])
        mkt_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(mkt_table)
        story.append(Spacer(1, 14))

    # Next Steps
    story.append(Paragraph("Recommended Action Plan", h2_style))
    steps = report.get('next_steps', [])
    for idx, step in enumerate(steps, 1):
        story.append(Paragraph(f"<b>{idx}.</b> {step}", body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
    story.append(Paragraph(report.get('disclaimer', ''), disclaimer_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_markdown(report: Dict[str, Any]) -> str:
    prefs = report.get('preferences', {})
    recs = report.get('recommended_properties', [])
    alts = report.get('alternative_properties', [])
    mkt = report.get('market_snapshot')

    md = []
    md.append("# AI Real Estate Explorer — Property & Market Report\n")
    md.append(f"**Report ID:** `{report.get('id')}`  ")
    md.append(f"**Generated Date:** {report.get('created_at', '')[:10]}  ")
    md.append(f"**Data Type:** {report.get('data_type', 'Demo Dataset')}\n")
    md.append("---\n")

    md.append("## 1. Search Criteria & User Requirements\n")
    md.append(f"- **Intent:** {str(prefs.get('intent', 'Buy')).title()}")
    md.append(f"- **Property Type:** {str(prefs.get('property_type', 'Any')).title()}")
    md.append(f"- **Location:** {prefs.get('area', '')} {prefs.get('city', '')} {prefs.get('country', '')}".strip() or "Any")
    if prefs.get('max_budget'):
        md.append(f"- **Max Budget:** {prefs.get('currency', 'PKR')} {prefs.get('max_budget', 0):,.0f}")
    if prefs.get('bedrooms'):
        md.append(f"- **Bedrooms:** {prefs.get('bedrooms')}")
    md.append(f"- **Total Qualified Matches:** {report.get('total_matches', 0)}\n")

    md.append("## 2. Top Recommended Properties\n")
    if recs:
        for idx, p in enumerate(recs, 1):
            md.append(f"### {idx}. {p.get('title')} ({p.get('match_score', 0)}% Match)")
            md.append(f"- **Price:** {p.get('currency', 'PKR')} {p.get('price', 0):,.0f}")
            md.append(f"- **Location:** {p.get('address', '')}")
            md.append(f"- **Configuration:** {p.get('bedrooms', 0)} Beds | {p.get('bathrooms', 0)} Baths | {p.get('covered_area_sqft', 0):,} sqft")
            if p.get('match_data', {}).get('positives'):
                md.append(f"- **Strengths:** {', '.join(p['match_data']['positives'])}")
            if p.get('match_data', {}).get('compromises'):
                md.append(f"- **Considerations:** {', '.join(p['match_data']['compromises'])}")
            md.append(f"- **Description:** {p.get('description', '')}\n")
    else:
        md.append("No direct recommendations found.\n")

    if alts:
        md.append("## 3. Alternative Matches\n")
        for p in alts:
            md.append(f"- **{p.get('title')}** ({p.get('currency', 'PKR')} {p.get('price', 0):,.0f}) — {p.get('area', '')}, {p.get('city', '')} ({p.get('match_score', 0)}% Match)")
        md.append("")

    if mkt:
        md.append("## 4. Market Intelligence Snapshot\n")
        md.append(f"- **Location:** {mkt.get('location_name', 'Market')}")
        md.append(f"- **Average Price (Sale):** {mkt.get('currency', 'PKR')} {mkt.get('avg_price_sale', 0):,.0f}")
        md.append(f"- **Median Price (Sale):** {mkt.get('currency', 'PKR')} {mkt.get('median_price_sale', 0):,.0f}")
        md.append(f"- **Price Per Sqft:** {mkt.get('currency', 'PKR')} {mkt.get('price_per_sqft_sale', 0):,.0f}")
        md.append(f"- **Demand Score:** {mkt.get('demand_score', 0)} / 100\n")

    md.append("## 5. Next Steps\n")
    for step in report.get('next_steps', []):
        md.append(f"1. {step}")
    md.append("\n---\n")
    md.append(f"> **Disclaimer:** {report.get('disclaimer', '')}\n")

    return "\n".join(md)

def generate_text(report: Dict[str, Any]) -> str:
    prefs = report.get('preferences', {})
    recs = report.get('recommended_properties', [])
    mkt = report.get('market_snapshot')

    lines = [
        "============================================================",
        "          AI REAL ESTATE EXPLORER — PROPERTY REPORT         ",
        "============================================================",
        f"Report ID: {report.get('id')}",
        f"Date:      {report.get('created_at', '')[:10]}",
        f"Intent:    {prefs.get('intent', 'Buy')}",
        f"City:      {prefs.get('city', 'All')}",
        "------------------------------------------------------------",
        "TOP RECOMMENDED PROPERTIES:",
    ]
    for idx, p in enumerate(recs, 1):
        lines.append(f"[{idx}] {p.get('title')}")
        lines.append(f"    Price:       {p.get('currency')} {p.get('price', 0):,.0f}")
        lines.append(f"    Location:    {p.get('area')}, {p.get('city')}")
        lines.append(f"    Layout:      {p.get('bedrooms')} Beds, {p.get('bathrooms')} Baths, {p.get('covered_area_sqft')} sqft")
        lines.append(f"    Match Score: {p.get('match_score')}%")
        lines.append("")

    if mkt:
        lines.append("------------------------------------------------------------")
        lines.append(f"MARKET DATA ({mkt.get('location_name')}):")
        lines.append(f"  Average Price:   {mkt.get('currency')} {mkt.get('avg_price_sale', 0):,.0f}")
        lines.append(f"  Demand Index:    {mkt.get('demand_score')}/100")
        lines.append("")

    lines.append("------------------------------------------------------------")
    lines.append("RECOMMENDED NEXT STEPS:")
    for idx, step in enumerate(report.get('next_steps', []), 1):
        lines.append(f"  {idx}. {step}")

    lines.append("------------------------------------------------------------")
    lines.append(f"NOTE: {report.get('disclaimer')}")
    lines.append("============================================================")

    return "\n".join(lines)
