from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render

from entretiens.models import Entretien

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from xml.sax.saxutils import escape

def liste_rapports(request):
    q = request.GET.get('q', "").strip()

    entretiens = Entretien.objects.select_related(
        'materiel', 'intervenant'
    ).order_by('materiel__numero', '-date_intervention')

    if q:
        entretiens = entretiens.filter(
            Q(materiel__numero__icontains=q) |
            Q(materiel__designation__icontains=q) |
            Q(intervenant__numero__icontains=q) |
            Q(intervenant__nom__icontains=q)
        )

    # Un groupe par matériel : ses interventions + ses totaux
    groupes = {}
    total_interventions = 0
    total_heures = Decimal('0')
    total_montant = Decimal('0')

    for e in entretiens:
        heures = Decimal(str(e.nombre_heures))
        taux = Decimal(str(e.intervenant.taux_horaire))
        montant = heures * taux          # ex. 2 h x 10 000 Ar/h = 20 000 Ar

        # Valeurs calculées, utilisées par le template
        e.taux = taux
        e.montant = montant

        groupe = groupes.setdefault(e.materiel_id, {
            'materiel': e.materiel,
            'interventions': [],
            'heures': Decimal('0'),
            'montant': Decimal('0'),
        })
        groupe['interventions'].append(e)
        groupe['heures'] += heures
        groupe['montant'] += montant

        total_interventions += 1
        total_heures += heures
        total_montant += montant

    return render(
        request,
        'rapport/rapport.html',
        {
            'rapports': list(groupes.values()),
            'q': q,
            'stats': {
                'materiels': len(groupes),
                'interventions': total_interventions,
                'heures': total_heures,
                'montant': total_montant,
            },
        }
    )


def exporter_rapport_pdf(request):

    q = request.GET.get('q', '').strip()

    entretiens = Entretien.objects.select_related(
        'materiel', 'intervenant'
    ).order_by('materiel__numero', '-date_intervention')

    if q:
        entretiens = entretiens.filter(
            Q(materiel__numero__icontains=q) |
            Q(materiel__designation__icontains=q) |
            Q(intervenant__numero__icontains=q) |
            Q(intervenant__nom__icontains=q)
        )

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'attachment; filename="rapport_interventions.pdf"'
    )

    pdf = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    elements = []

    styles = getSampleStyleSheet()

    titre = ParagraphStyle(
        'Titre',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=25
    )

    elements.append(
        Paragraph("RAPPORT DES PRESTATIONS", titre)
    )

    elements.append(Spacer(1, 15))

    donnees = [
        [
            'Numéro matériel',
            'Nom de l\'intervenant',
            'Montant des prestations'
        ]
    ]

    total = Decimal('0')

    for e in entretiens:

        heures = Decimal(str(e.nombre_heures))
        taux = Decimal(str(e.intervenant.taux_horaire))

        montant = heures * taux

        total += montant

        donnees.append([
            str(e.materiel.numero),
            str(e.intervenant.nom),
            f"{montant:,.0f}".replace(',', ' ') + " Ar"
        ])

    # Ligne du montant total
    donnees.append([
        '',
        'TOTAL DES PRESTATIONS',
        f"{total:,.0f}".replace(',', ' ') + " Ar"
    ])

    tableau = Table(
        donnees,
        colWidths=[5*cm, 6*cm, 6*cm],
        repeatRows=1
    )

    tableau.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0),
         colors.HexColor('#263B5E')),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BACKGROUND', (0, -1), (-1, -1),
         colors.HexColor('#DCE6F1')),

        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('TOPPADDING', (0, 0), (-1, -1), 12),

        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

    ]))

    elements.append(tableau)

    pdf.build(elements)

    return response
