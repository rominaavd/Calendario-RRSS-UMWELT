import json
import re

with open('calendario-ig-standalone.backup.html', 'r', encoding='utf-8') as f:
    orig = f.read()

logo_m = re.search(r'src=\"(data:image/png;base64,[^\"]+)\"', orig)
data_m = re.search(r'<script id=\"data\" type=\"application/json\">(.*?)</script>', orig, re.DOTALL)

logo = logo_m.group(1) if logo_m else ''
initial_json = data_m.group(1).strip() if data_m else '{"posts": [], "_selMonth": "2026-09"}'

html_template = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Calendario de Contenido RRSS | UMWELT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-display: 'Outfit', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      /* Light Theme (Warm Natural UMWELT Aesthetic) */
      --bg: #f8f6f0;
      --bg-subtle: #f1ede3;
      --card: #ffffff;
      --card-alt: #fdfcf9;
      --card-border: #e8e2d5;
      --card-border-hover: #d2c8b6;
      --ink: #23211e;
      --ink-soft: #57524a;
      --ink-muted: #8b857a;
      
      /* Primary Brand: Terracotta / Orange UMWELT */
      --orange: #e8590c;
      --orange-hover: #d04c04;
      --orange-soft: #fff1e6;
      --orange-border: #ffd8bf;
      
      /* Accent Green: Forest & Nature */
      --green: #409121;
      --green-hover: #337619;
      --green-soft: #eef8eb;
      --green-border: #c8ebb9;
      
      /* Status Colors */
      --status-pend-bg: #fff8e6;
      --status-pend-text: #b7791f;
      --status-pend-border: #fde68a;

      --status-prog-bg: #eff6ff;
      --status-prog-text: #2563eb;
      --status-prog-border: #bfdbfe;

      --status-listo-bg: #ecfdf5;
      --status-listo-text: #16a34a;
      --status-listo-border: #bbf7d0;

      --status-fail-bg: #fef2f2;
      --status-fail-text: #dc2626;
      --status-fail-border: #fecaca;

      /* Post Type Colors */
      --type-reel: #7c3aed;
      --type-reel-bg: #f5f3ff;
      --type-post: #0284c7;
      --type-post-bg: #f0f9ff;
      --type-carrousel: #db2777;
      --type-carrousel-bg: #fdf2f8;
      --type-story: #d97706;
      --type-story-bg: #fffbeb;

      --shadow-sm: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
      --shadow-md: 0 4px 14px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
      --shadow-lg: 0 10px 30px rgba(0,0,0,0.08), 0 3px 8px rgba(0,0,0,0.04);
      --shadow-pop: 0 20px 45px rgba(0,0,0,0.14);

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-xl: 22px;
      --radius-full: 9999px;

      --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    [data-theme="dark"] {{
      --bg: #141311;
      --bg-subtle: #1c1b18;
      --card: #201e1a;
      --card-alt: #262420;
      --card-border: #36322b;
      --card-border-hover: #4d483e;
      --ink: #f5f2eb;
      --ink-soft: #c2bbb0;
      --ink-muted: #8c8578;

      --orange-soft: #382013;
      --orange-border: #5a2e16;
      --green-soft: #1a2a14;
      --green-border: #2c4a20;

      --status-pend-bg: #322610;
      --status-pend-text: #f6c453;
      --status-pend-border: #4d3b14;

      --status-prog-bg: #122842;
      --status-prog-text: #60a5fa;
      --status-prog-border: #1e3d64;

      --status-listo-bg: #112e1d;
      --status-listo-text: #4ade80;
      --status-listo-border: #194f2e;

      --status-fail-bg: #3b1818;
      --status-fail-text: #f87171;
      --status-fail-border: #5c2222;

      --type-reel-bg: #2b1842;
      --type-post-bg: #102a3d;
      --type-carrousel-bg: #3b1328;
      --type-story-bg: #3d240a;

      --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
      --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
      --shadow-lg: 0 12px 36px rgba(0,0,0,0.5);
      --shadow-pop: 0 20px 50px rgba(0,0,0,0.7);
    }}

    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --bg: #141311;
        --bg-subtle: #1c1b18;
        --card: #201e1a;
        --card-alt: #262420;
        --card-border: #36322b;
        --card-border-hover: #4d483e;
        --ink: #f5f2eb;
        --ink-soft: #c2bbb0;
        --ink-muted: #8c8578;

        --orange-soft: #382013;
        --orange-border: #5a2e16;
        --green-soft: #1a2a14;
        --green-border: #2c4a20;

        --status-pend-bg: #322610;
        --status-pend-text: #f6c453;
        --status-pend-border: #4d3b14;

        --status-prog-bg: #122842;
        --status-prog-text: #60a5fa;
        --status-prog-border: #1e3d64;

        --status-listo-bg: #112e1d;
        --status-listo-text: #4ade80;
        --status-listo-border: #194f2e;

        --status-fail-bg: #3b1818;
        --status-fail-text: #f87171;
        --status-fail-border: #5c2222;

        --type-reel-bg: #2b1842;
        --type-post-bg: #102a3d;
        --type-carrousel-bg: #3b1328;
        --type-story-bg: #3d240a;

        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
        --shadow-lg: 0 12px 36px rgba(0,0,0,0.5);
        --shadow-pop: 0 20px 50px rgba(0,0,0,0.7);
      }}
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-main);
      background-color: var(--bg);
      color: var(--ink);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      padding: 24px 32px 60px;
      max-width: 1440px;
      margin: 0 auto;
      min-height: 100vh;
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    /* Top Utility Header */
    .top-navbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .logo-container {{
      background: linear-gradient(135deg, var(--card), var(--bg-subtle));
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
      cursor: pointer;
    }}

    .logo-container:hover {{
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
      border-color: var(--orange);
    }}

    .logo-container img {{
      width: 44px;
      height: 44px;
      object-fit: contain;
      display: block;
    }}

    .brand-text h1 {{
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin: 0 0 2px 0;
      color: var(--ink);
    }}

    .brand-text .brand-subtitle {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--ink-soft);
      font-weight: 500;
      flex-wrap: wrap;
    }}

    .storage-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 11px;
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      text-decoration: none;
    }}

    .storage-badge.live-connected {{
      background: var(--green-soft);
      color: var(--green);
      border: 1px solid var(--green-border);
    }}

    .storage-badge.live-offline {{
      background: var(--status-pend-bg);
      color: var(--status-pend-text);
      border: 1px solid var(--status-pend-border);
    }}

    .storage-badge:hover {{
      transform: scale(1.02);
      filter: brightness(0.97);
    }}

    .storage-pulse {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--green);
      box-shadow: 0 0 0 0 rgba(64, 145, 33, 0.7);
      animation: pulse-green 2s infinite;
    }}

    @keyframes pulse-green {{
      0% {{ box-shadow: 0 0 0 0 rgba(64, 145, 33, 0.7); }}
      70% {{ box-shadow: 0 0 0 6px rgba(64, 145, 33, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(64, 145, 33, 0); }}
    }}

    /* Global Header Actions */
    .top-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .btn {{
      font-family: var(--font-main);
      font-size: 13.5px;
      font-weight: 600;
      padding: 9px 16px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--card);
      color: var(--ink);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: var(--transition);
      box-shadow: var(--shadow-sm);
    }}

    .btn:hover {{
      border-color: var(--card-border-hover);
      background: var(--card-alt);
      transform: translateY(-1px);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, var(--orange), #f37b2d);
      border-color: var(--orange);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(232, 89, 12, 0.28);
    }}

    .btn-primary:hover {{
      background: linear-gradient(135deg, var(--orange-hover), #e8590c);
      border-color: var(--orange-hover);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(232, 89, 12, 0.35);
    }}

    .btn-sync {{
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      border-color: #2563eb;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }}

    .btn-sync:hover {{
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      border-color: #1d4ed8;
      color: #ffffff;
    }}

    .btn-secondary {{
      background: var(--card);
      border-color: var(--card-border);
      color: var(--ink);
    }}

    .btn-icon {{
      padding: 9px 12px;
    }}

    /* Tabs & Controls Section */
    .controls-panel {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 22px;
      background: var(--card);
      border: 1px solid var(--card-border);
      padding: 10px 14px;
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
    }}

    .view-tabs {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
    }}

    .view-tab {{
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13.5px;
      font-weight: 600;
      color: var(--ink-soft);
      cursor: pointer;
      background: transparent;
      border: none;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: var(--transition);
    }}

    .view-tab:hover {{
      color: var(--ink);
    }}

    .view-tab.active {{
      background: var(--card);
      color: var(--orange);
      box-shadow: var(--shadow-sm);
    }}

    .search-filter-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
      max-width: 520px;
      justify-content: flex-end;
      flex-wrap: wrap;
    }}

    .search-box {{
      position: relative;
      flex: 1;
      min-width: 190px;
    }}

    .search-box input {{
      width: 100%;
      font-family: var(--font-main);
      font-size: 13px;
      padding: 8px 12px 8px 32px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--bg-subtle);
      color: var(--ink);
      outline: none;
      transition: var(--transition);
    }}

    .search-box input:focus {{
      background: var(--card);
      border-color: var(--orange);
      box-shadow: 0 0 0 3px rgba(232, 89, 12, 0.12);
    }}

    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 13px;
      color: var(--ink-muted);
      pointer-events: none;
    }}

    .filter-select {{
      font-family: var(--font-main);
      font-size: 13px;
      padding: 8px 12px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--bg-subtle);
      color: var(--ink);
      font-weight: 500;
      outline: none;
      cursor: pointer;
      transition: var(--transition);
    }}

    .filter-select:focus {{
      border-color: var(--orange);
    }}

    /* Global Info & Quick Stats Bar */
    .quick-stats-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 20px;
      font-size: 13px;
      color: var(--ink-soft);
      flex-wrap: wrap;
    }}

    .stats-pills {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .stat-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 600;
      background: var(--card);
      border: 1px solid var(--card-border);
      color: var(--ink);
      cursor: pointer;
      transition: var(--transition);
    }}

    .stat-badge:hover {{
      border-color: var(--card-border-hover);
      transform: translateY(-1px);
    }}

    .stat-badge.filter-active {{
      border-color: var(--orange);
      background: var(--orange-soft);
      color: var(--orange);
    }}

    /* --- WEEK VIEW (SEMANA) --- */
    .weeknav-container {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
      flex-wrap: wrap;
    }}

    .weeknav-controls {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .nav-btn {{
      font-family: var(--font-main);
      font-size: 13.5px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--card);
      color: var(--ink);
      cursor: pointer;
      transition: var(--transition);
    }}

    .nav-btn:hover {{
      border-color: var(--orange);
      color: var(--orange);
      background: var(--card-alt);
    }}

    .week-label {{
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 17px;
      color: var(--ink);
      padding: 0 6px;
    }}

    .today-pill {{
      font-size: 12px;
      color: var(--green);
      font-weight: 700;
      background: var(--green-soft);
      border: 1px solid var(--green-border);
      padding: 4px 12px;
      border-radius: var(--radius-full);
    }}

    .grid-week {{
      display: grid;
      grid-template-columns: repeat(7, minmax(170px, 1fr));
      gap: 14px;
      align-items: start;
      overflow-x: auto;
      padding-bottom: 12px;
    }}

    .day-col {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 14px;
      min-width: 170px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: var(--transition);
      position: relative;
    }}

    .day-col:hover {{
      border-color: var(--card-border-hover);
      box-shadow: var(--shadow-md);
    }}

    .day-col.is-today {{
      border-color: var(--orange);
      box-shadow: 0 0 0 1.5px var(--orange), var(--shadow-sm);
      background: linear-gradient(180deg, var(--card-alt) 0%, var(--card) 100%);
    }}

    .day-col-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--card-border);
    }}

    .day-name-block {{
      display: flex;
      flex-direction: column;
    }}

    .day-name {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--ink-muted);
    }}

    .day-number {{
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.1;
    }}

    .day-count-badge {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-full);
      background: var(--bg-subtle);
      color: var(--ink-soft);
      border: 1px solid var(--card-border);
    }}

    .day-col.is-today .day-count-badge {{
      background: var(--orange-soft);
      color: var(--orange);
      border-color: var(--orange-border);
    }}

    .posts-container {{
      display: flex;
      flex-direction: column;
      gap: 9px;
      min-height: 40px;
    }}

    /* Card Post Styling */
    .post-card {{
      background: var(--card-alt);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 10px 11px;
      cursor: pointer;
      position: relative;
      transition: var(--transition);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .post-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--orange);
    }}

    .post-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
    }}

    .type-badge {{
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 2px 7px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .type-Reel {{ background: var(--type-reel-bg); color: var(--type-reel); }}
    .type-Post {{ background: var(--type-post-bg); color: var(--type-post); }}
    .type-Carrusel {{ background: var(--type-carrousel-bg); color: var(--type-carrousel); }}
    .type-Story {{ background: var(--type-story-bg); color: var(--type-story); }}

    .post-card-actions {{
      display: flex;
      align-items: center;
      gap: 5px;
      opacity: 0.7;
      transition: var(--transition);
    }}

    .post-card:hover .post-card-actions {{
      opacity: 1;
    }}

    .action-icon {{
      font-size: 13px;
      cursor: pointer;
      padding: 2px;
      border-radius: 4px;
      color: var(--ink-muted);
      transition: var(--transition);
      line-height: 1;
    }}

    .action-icon:hover {{
      color: var(--orange);
      transform: scale(1.15);
    }}

    .post-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.35;
      word-break: break-word;
    }}

    .post-notes {{
      font-size: 11px;
      color: var(--ink-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      width: fit-content;
      transition: var(--transition);
      border: 1px solid transparent;
      user-select: none;
    }}

    .status-pill:hover {{
      filter: brightness(0.95);
      transform: scale(1.02);
    }}

    .st-pendiente {{ background: var(--status-pend-bg); color: var(--status-pend-text); border-color: var(--status-pend-border); }}
    .st-en_progreso {{ background: var(--status-prog-bg); color: var(--status-prog-text); border-color: var(--status-prog-border); }}
    .st-listo {{ background: var(--status-listo-bg); color: var(--status-listo-text); border-color: var(--status-listo-border); }}
    .st-no_realizado {{ background: var(--status-fail-bg); color: var(--status-fail-text); border-color: var(--status-fail-border); }}

    .btn-add-day {{
      width: 100%;
      background: var(--bg-subtle);
      border: 1px dashed var(--card-border);
      border-radius: var(--radius-md);
      padding: 8px 10px;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--ink-soft);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: var(--transition);
      margin-top: 4px;
    }}

    .btn-add-day:hover {{
      border-color: var(--orange);
      color: var(--orange);
      background: var(--card-alt);
    }}

    /* --- PLANNER / MONTH GRID VIEW --- */
    .month-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      gap: 14px;
      flex-wrap: wrap;
    }}

    .month-selector-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .month-selector-group select {{
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--card);
      color: var(--ink);
      cursor: pointer;
      outline: none;
    }}

    .month-selector-group select:focus {{
      border-color: var(--orange);
    }}

    .planner-weekdays-row {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 10px;
      margin-bottom: 8px;
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      text-align: center;
    }}

    .planner-calendar-grid {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 10px;
    }}

    .planner-cell {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 10px;
      min-height: 125px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: var(--transition);
      box-shadow: var(--shadow-sm);
    }}

    .planner-cell:hover {{
      box-shadow: var(--shadow-md);
      border-color: var(--card-border-hover);
    }}

    .planner-cell.dim {{
      opacity: 0.45;
      background: var(--bg-subtle);
    }}

    .planner-cell.is-today {{
      border-color: var(--orange);
      box-shadow: 0 0 0 1.5px var(--orange) inset, var(--shadow-sm);
      background: linear-gradient(180deg, var(--card-alt) 0%, var(--card) 100%);
    }}

    .planner-cell-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .planner-day-num {{
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: var(--ink);
    }}

    .planner-add-mini {{
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-muted);
      cursor: pointer;
      padding: 2px 5px;
      border-radius: 4px;
      line-height: 1;
      opacity: 0;
      transition: var(--transition);
    }}

    .planner-cell:hover .planner-add-mini {{
      opacity: 1;
      color: var(--orange);
      background: var(--orange-soft);
    }}

    .planner-chips-list {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      flex: 1;
      overflow-y: auto;
      max-height: 140px;
    }}

    .planner-chip {{
      font-size: 11px;
      font-weight: 600;
      padding: 3px 7px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transition: var(--transition);
      border: 1px solid transparent;
    }}

    .planner-chip:hover {{
      transform: translateY(-1px);
      box-shadow: var(--shadow-sm);
    }}

    .planner-chip-title {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    /* --- DASHBOARD / MONTH BREAKDOWN VIEW --- */
    .dashboard-metrics-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}

    .metric-card {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
      position: relative;
      overflow: hidden;
    }}

    .metric-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--card-border-hover);
    }}

    .metric-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--card-border);
    }}

    .metric-card.m-total::before {{ background: var(--ink-soft); }}
    .metric-card.m-listo::before {{ background: var(--green); }}
    .metric-card.m-prog::before {{ background: #2563eb; }}
    .metric-card.m-pend::before {{ background: #e0901e; }}
    .metric-card.m-fail::before {{ background: #dc2626; }}

    .metric-num {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 800;
      line-height: 1;
    }}

    .metric-label {{
      font-size: 12.5px;
      color: var(--ink-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .progress-bar-container {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}

    .progress-bar-info {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13.5px;
      font-weight: 600;
      margin-bottom: 10px;
    }}

    .progress-track {{
      height: 12px;
      background: var(--bg-subtle);
      border-radius: var(--radius-full);
      overflow: hidden;
      display: flex;
    }}

    .progress-fill-listo {{ background: var(--green); height: 100%; transition: width 0.4s ease; }}
    .progress-fill-prog {{ background: #3b82f6; height: 100%; transition: width 0.4s ease; }}
    .progress-fill-pend {{ background: #f59e0b; height: 100%; transition: width 0.4s ease; }}
    .progress-fill-fail {{ background: #ef4444; height: 100%; transition: width 0.4s ease; }}

    /* Table Breakdown */
    .table-container {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      text-align: left;
    }}

    table.data-table th {{
      background: var(--bg-subtle);
      color: var(--ink-muted);
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 12px 16px;
      border-bottom: 1px solid var(--card-border);
    }}

    table.data-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--card-border);
      color: var(--ink);
    }}

    table.data-table tr:last-child td {{
      border-bottom: none;
    }}

    table.data-table tr:hover td {{
      background: var(--card-alt);
    }}

    /* Modals & Dialogs */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
      z-index: 1000;
      animation: fadeIn 0.15s ease;
    }}

    .modal-backdrop.active {{
      display: flex;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}

    .modal-window {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-xl);
      width: 100%;
      max-width: 540px;
      box-shadow: var(--shadow-pop);
      overflow: hidden;
      animation: slideUp 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes slideUp {{
      from {{ transform: translateY(15px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 24px;
      border-bottom: 1px solid var(--card-border);
    }}

    .modal-header h3 {{
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 700;
      margin: 0;
    }}

    .modal-close {{
      background: transparent;
      border: none;
      font-size: 18px;
      color: var(--ink-muted);
      cursor: pointer;
      padding: 4px;
      line-height: 1;
      border-radius: 6px;
    }}

    .modal-close:hover {{
      color: var(--ink);
      background: var(--bg-subtle);
    }}

    .modal-body {{
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      max-height: 80vh;
      overflow-y: auto;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .form-group label {{
      font-size: 12.5px;
      font-weight: 600;
      color: var(--ink-soft);
    }}

    .form-group input, .form-group select, .form-group textarea {{
      font-family: var(--font-main);
      font-size: 13.5px;
      padding: 10px 12px;
      border-radius: var(--radius-md);
      border: 1px solid var(--card-border);
      background: var(--bg-subtle);
      color: var(--ink);
      outline: none;
      transition: var(--transition);
    }}

    .form-group input:focus, .form-group select:focus, .form-group textarea:focus {{
      background: var(--card);
      border-color: var(--orange);
      box-shadow: 0 0 0 3px rgba(232, 89, 12, 0.12);
    }}

    .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    .modal-footer {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 10px;
      padding: 16px 24px;
      background: var(--bg-subtle);
      border-top: 1px solid var(--card-border);
    }}

    /* Toast Notifications */
    .toast-container {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 2000;
      pointer-events: none;
    }}

    .toast {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 12px 18px;
      font-size: 13.5px;
      font-weight: 600;
      color: var(--ink);
      box-shadow: var(--shadow-lg);
      display: flex;
      align-items: center;
      gap: 10px;
      pointer-events: auto;
      animation: toastIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes toastIn {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Footer / Legend */
    .footer-bar {{
      margin-top: 36px;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      font-size: 12.5px;
      color: var(--ink-muted);
    }}

    .legend-chips {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .legend-chip {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      body {{
        padding: 16px 16px 40px;
      }}
      .brand-section {{
        width: 100%;
      }}
      .top-actions {{
        width: 100%;
        justify-content: stretch;
      }}
      .top-actions .btn {{
        flex: 1;
        justify-content: center;
      }}
      .controls-panel {{
        flex-direction: column;
        align-items: stretch;
      }}
      .search-filter-wrap {{
        max-width: none;
      }}
      .grid-week {{
        grid-template-columns: 1fr;
      }}
      .planner-weekdays-row {{
        display: none;
      }}
      .planner-calendar-grid {{
        grid-template-columns: 1fr;
      }}
      .planner-cell {{
        min-height: auto;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Navigation & Brand Header -->
  <header class="top-navbar">
    <div class="brand-section">
      <div class="logo-container" onclick="openSyncModal()" title="UMWELT - Haz clic para ver estado de sincronización">
        <img src="{logo}" alt="Logo UMWELT">
      </div>
      <div class="brand-text">
        <h1>Calendario Editorial RRSS</h1>
        <div class="brand-subtitle">
          <span>UMWELT • Instagram</span>
          <span class="storage-badge live-offline" onclick="openSyncModal()" id="storage-status-pill" title="Haz clic para configurar sincronización con tu equipo">
            <span class="storage-pulse"></span>
            <span id="storage-status-text">⚡ Conectar Sincronización en Vivo</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="top-actions">
      <button class="btn btn-sync" onclick="openSyncModal()" title="Conectar o revisar sincronización con el equipo">
        <span>⚡</span> Sincronización Equipo
      </button>
      <button class="btn btn-primary" onclick="saveHtmlFile()" title="Guarda o descarga el archivo HTML con todos tus cambios para compartirlo">
        <span>💾</span> Guardar Archivo HTML
      </button>
      <button class="btn btn-secondary" onclick="exportExcel()" title="Descarga la planilla completa en Excel">
        <span>📊</span> Exportar Excel
      </button>
      <button class="btn btn-secondary" onclick="openShareModal()" title="Opciones de respaldo y enlace">
        <span>⚙️</span> Opciones
      </button>
      <button class="btn btn-icon btn-secondary" onclick="toggleTheme()" id="theme-btn" title="Alternar Modo Oscuro / Claro">
        🌓
      </button>
    </div>
  </header>

  <!-- Controls Panel (Tabs, Search & Filters) -->
  <div class="controls-panel">
    <div class="view-tabs">
      <button class="view-tab active" data-tab="semana" onclick="setTab('semana')">
        <span>📅</span> Vista Semanal
      </button>
      <button class="view-tab" data-tab="planner" onclick="setTab('planner')">
        <span>🗓️</span> Calendario Mensual
      </button>
      <button class="view-tab" data-tab="mes" onclick="setTab('mes')">
        <span>📊</span> Desglose & Métricas
      </button>
    </div>

    <div class="search-filter-wrap">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="search-input" placeholder="Buscar por tema o título..." oninput="handleSearch(this.value)">
      </div>
      <select class="filter-select" id="filter-type" onchange="handleFilterType(this.value)">
        <option value="all">Todos los formatos</option>
        <option value="Reel">🎬 Reel</option>
        <option value="Carrusel">🎠 Carrusel</option>
        <option value="Post">🖼️ Post</option>
        <option value="Story">📱 Story</option>
      </select>
      <select class="filter-select" id="filter-status" onchange="handleFilterStatus(this.value)">
        <option value="all">Todos los estados</option>
        <option value="pendiente">⏳ Pendiente</option>
        <option value="en_progreso">🔄 En progreso</option>
        <option value="listo">✅ Listo</option>
        <option value="no_realizado">❌ No realizado</option>
      </select>
    </div>
  </div>

  <!-- Quick Status Filter Pills -->
  <div class="quick-stats-bar">
    <div class="stats-pills">
      <span style="font-weight:600; margin-right:4px;">Filtrado rápido:</span>
      <span class="stat-badge" onclick="quickFilterStatus('all')" id="qf-all">Todos (<span id="count-total">0</span>)</span>
      <span class="stat-badge" onclick="quickFilterStatus('listo')" id="qf-listo">✅ Listos (<span id="count-listo">0</span>)</span>
      <span class="stat-badge" onclick="quickFilterStatus('en_progreso')" id="qf-prog">🔄 En progreso (<span id="count-prog">0</span>)</span>
      <span class="stat-badge" onclick="quickFilterStatus('pendiente')" id="qf-pend">⏳ Pendientes (<span id="count-pend">0</span>)</span>
      <span class="stat-badge" onclick="quickFilterStatus('no_realizado')" id="qf-fail">❌ No realizados (<span id="count-fail">0</span>)</span>
    </div>
    <div id="filter-notice" style="display:none; color:var(--orange); font-weight:600;">
      <span>Filtro activo</span> • <a href="javascript:void(0)" onclick="clearFilters()" style="color:inherit; text-decoration:underline;">Limpiar filtros</a>
    </div>
  </div>

  <!-- View 1: Semana -->
  <div id="view-semana"></div>

  <!-- View 2: Planner Mensual -->
  <div id="view-planner" style="display:none;"></div>

  <!-- View 3: Desglose / Dashboard Mensual -->
  <div id="view-mes" style="display:none;"></div>

  <!-- Footer / Leyenda -->
  <footer class="footer-bar">
    <div class="legend-chips">
      <span class="legend-chip">⏳ Pendiente</span>
      <span class="legend-chip">🔄 En progreso</span>
      <span class="legend-chip">✅ Listo</span>
      <span class="legend-chip">❌ No realizado</span>
      <span class="legend-chip" style="margin-left: 8px;">🔒 Historia diaria obligatoria</span>
    </div>
    <div>
      <span>UMWELT • Calendario RRSS • Clic en cualquier publicación para avanzar su estado</span>
    </div>
  </footer>

  <!-- Modal: Agregar / Editar Publicación -->
  <div class="modal-backdrop" id="post-modal" onclick="handleBackdropClick(event, 'post-modal')">
    <div class="modal-window">
      <div class="modal-header">
        <h3 id="modal-title">Nueva Publicación</h3>
        <button class="modal-close" onclick="closeModal('post-modal')">✕</button>
      </div>
      <div class="modal-body">
        <input type="hidden" id="form-post-id">
        <div class="form-row">
          <div class="form-group">
            <label for="form-date">Fecha de Publicación</label>
            <input type="date" id="form-date" required>
          </div>
          <div class="form-group">
            <label for="form-type">Formato / Tipo</label>
            <select id="form-type">
              <option value="Reel">🎬 Reel</option>
              <option value="Carrusel">🎠 Carrusel</option>
              <option value="Post">🖼️ Post</option>
              <option value="Story">📱 Story</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label for="form-title">Título o Tema del Contenido</label>
          <input type="text" id="form-title" placeholder="Ej: Lanzamiento nueva colección, Tips de reciclaje..." required>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="form-status">Estado</label>
            <select id="form-status">
              <option value="pendiente">⏳ Pendiente</option>
              <option value="en_progreso">🔄 En progreso</option>
              <option value="listo">✅ Listo</option>
              <option value="no_realizado">❌ No realizado</option>
            </select>
          </div>
          <div class="form-group">
            <label for="form-time">Hora sugerida / Formato adicional</label>
            <input type="text" id="form-time" placeholder="Ej: 19:00 hrs, Colaboración...">
          </div>
        </div>

        <div class="form-group">
          <label for="form-notes">Notas / Copy / Instrucciones (Opcional)</label>
          <textarea id="form-notes" rows="2" placeholder="Detalles de diseño, hashtags o copy..."></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="closeModal('post-modal')">Cancelar</button>
        <button class="btn btn-primary" onclick="submitPostModal()">Guardar Publicación</button>
      </div>
    </div>
  </div>

  <!-- Modal: Sincronización en Vivo con el Equipo (Google Sheets / Webhook) -->
  <div class="modal-backdrop" id="sync-modal" onclick="handleBackdropClick(event, 'sync-modal')">
    <div class="modal-window">
      <div class="modal-header">
        <h3>⚡ Sincronización en Vivo con el Equipo</h3>
        <button class="modal-close" onclick="closeModal('sync-modal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="background:var(--bg-subtle); border:1px solid var(--card-border); border-radius:var(--radius-md); padding:14px; display:flex; flex-direction:column; gap:8px;">
          <div style="font-weight:700; font-size:13.5px; color:var(--ink);">
            ¿Cómo conectar para que todos editen en tiempo real?
          </div>
          <div style="font-size:12.5px; color:var(--ink-soft); line-height:1.5;">
            Conecta una planilla de Google Sheets usando Google Apps Script. <strong>Cualquier cambio que tú o tu equipo hagan se reflejará al instante para todos</strong> y se guardará ordenado en Google Drive.
          </div>
        </div>

        <div class="form-group">
          <label for="sync-url-input">URL de la Aplicación Web (terminada en /exec):</label>
          <input type="text" id="sync-url-input" placeholder="https://script.google.com/macros/s/.../exec">
        </div>

        <div style="display:flex; gap:8px;">
          <button class="btn btn-primary" style="flex:1;" onclick="saveSyncUrl()">
            Guardar y Conectar
          </button>
          <button class="btn btn-secondary" onclick="testSyncConnection()">
            Probar Conexión
          </button>
        </div>

        <div style="margin-top:6px; border-top:1px solid var(--card-border); padding-top:12px; display:flex; flex-direction:column; gap:8px;">
          <div style="font-size:12px; font-weight:700; color:var(--ink);">Pasos rápidos (Toma 1 minuto):</div>
          <ol style="font-size:12px; color:var(--ink-soft); padding-left:18px; line-height:1.6;">
            <li>Abre <a href="https://sheets.new" target="_blank" style="color:var(--orange); font-weight:600;">sheets.new</a> en tu navegador.</li>
            <li>Ve a <strong>Extensiones > Apps Script</strong>.</li>
            <li>Pega el código sincronizador del archivo <code style="font-family:var(--font-mono); font-size:11px;">codigo_google_sheets.js</code>.</li>
            <li>Haz clic en <strong>Implementar > Nueva implementación > Aplicación web</strong>.</li>
            <li>Acceso: <em>"Cualquier persona" (Anyone)</em>. Copia la URL /exec y pégala arriba.</li>
          </ol>
          <button class="btn btn-secondary" style="font-size:12px; padding:6px 10px;" onclick="copyScriptCode()">
            📋 Copiar código de Google Apps Script al portapapeles
          </button>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="closeModal('sync-modal')">Cerrar</button>
      </div>
    </div>
  </div>

  <!-- Modal: Opciones Generales de Respaldo -->
  <div class="modal-backdrop" id="share-modal" onclick="handleBackdropClick(event, 'share-modal')">
    <div class="modal-window">
      <div class="modal-header">
        <h3>Opciones y Respaldo</h3>
        <button class="modal-close" onclick="closeModal('share-modal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="display:flex; flex-direction:column; gap:10px;">
          <button class="btn btn-primary" onclick="saveHtmlFile(); closeModal('share-modal');">
            💾 Guardar / Descargar archivo HTML actualizado
          </button>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <button class="btn btn-secondary" onclick="exportJsonBackup()">
              📥 Exportar JSON
            </button>
            <button class="btn btn-secondary" onclick="triggerImportJson()">
              📤 Importar JSON
            </button>
          </div>
          <input type="file" id="json-file-input" accept=".json" style="display:none" onchange="importJsonFile(event)">
          <button class="btn btn-secondary" onclick="copyShareableUrl()">
            🔗 Copiar enlace con todos los datos incrustados
          </button>
          <button class="btn btn-secondary" onclick="resetToInitialData()" style="color:var(--status-fail-text); border-color:var(--status-fail-border);">
            🔄 Restablecer plantilla inicial
          </button>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="closeModal('share-modal')">Cerrar</button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div class="toast-container" id="toast-container"></div>

  <!-- INITIAL EMBEDDED DATA -->
  <script id="data" type="application/json">{initial_json}</script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

  <script>
    // --- STATE INITIALIZATION & LOCALSTORAGE ---
    const STORAGE_KEY = 'umwelt_rrss_calendar_data_v2';
    const THEME_KEY = 'umwelt_theme_preference';
    const SYNC_URL_KEY = 'umwelt_sync_url_v1';

    // Embedded sync URL that will be injected when the user clicks "Guardar Archivo HTML"
    let EMBEDDED_SYNC_URL = '';

    let SYNC_URL = localStorage.getItem(SYNC_URL_KEY) || EMBEDDED_SYNC_URL || '';

    let STATE = {{
      posts: [],
      _selMonth: '2026-09'
    }};

    function isLiveSyncActive() {{
      return SYNC_URL && SYNC_URL.trim().startsWith('http');
    }}

    function updateStorageBadge() {{
      const pill = document.getElementById('storage-status-pill');
      const text = document.getElementById('storage-status-text');
      const pulse = document.querySelector('.storage-pulse');

      if (isLiveSyncActive()) {{
        pill.className = 'storage-badge live-connected';
        text.textContent = '🟢 Sincronizado en Vivo (Equipo)';
        pulse.style.backgroundColor = 'var(--green)';
        pill.title = 'Conectado a la base de datos compartida. Todos ven los mismos cambios.';
      }} else {{
        pill.className = 'storage-badge live-offline';
        text.textContent = '⚡ Conectar Sincronización en Vivo';
        pulse.style.backgroundColor = '#e0901e';
        pill.title = 'Haz clic para conectar con tu equipo y ver cambios en tiempo real.';
      }}
    }}

    // Load state prioritizing LocalStorage, then URL hash data, then embedded script tag
    function initState() {{
      // 1. Try URL hash share data if present
      if (window.location.hash && window.location.hash.startsWith('#data=')) {{
        try {{
          const rawHash = decodeURIComponent(window.location.hash.slice(6));
          const parsed = JSON.parse(rawHash);
          if (parsed && Array.isArray(parsed.posts)) {{
            STATE = parsed;
            saveToStorage();
            showToast('🔗 Datos cargados exitosamente desde el enlace compartido.');
            history.replaceState(null, null, ' ');
            return;
          }}
        }} catch(e) {{
          console.warn('Error leyendo datos desde URL:', e);
        }}
      }}

      // 2. Try localStorage
      const local = localStorage.getItem(STORAGE_KEY);
      if (local) {{
        try {{
          const parsed = JSON.parse(local);
          if (parsed && Array.isArray(parsed.posts) && parsed.posts.length > 0) {{
            STATE = parsed;
            return;
          }}
        }} catch(e) {{
          console.warn('Error leyendo localStorage:', e);
        }}
      }}

      // 3. Fallback to embedded script
      try {{
        const embedded = JSON.parse(document.getElementById('data').textContent);
        if (embedded && Array.isArray(embedded.posts)) {{
          STATE = embedded;
          saveToStorage();
        }}
      }} catch(e) {{
        console.error('Error parseando datos iniciales:', e);
      }}
    }}

    function saveToStorage() {{
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(STATE));
        updateStorageBadge();
      }} catch(e) {{
        console.error('Error guardando en localStorage:', e);
      }}
    }}

    // --- LIVE TEAM SYNC (GOOGLE APPS SCRIPT / CLOUD) ---
    let syncInFlight = false;

    async function loadFromCloud(silent = false) {{
      if (!isLiveSyncActive()) return;
      try {{
        const res = await fetch(SYNC_URL, {{ redirect: 'follow' }});
        const data = await res.json();
        if (data && Array.isArray(data.posts) && data.posts.length > 0) {{
          const localStr = JSON.stringify(STATE.posts);
          const remoteStr = JSON.stringify(data.posts);
          if (localStr !== remoteStr) {{
            STATE.posts = data.posts;
            if (data._selMonth) STATE._selMonth = data._selMonth;
            saveToStorage();
            render();
            if (!silent) showToast('🔔 Calendario actualizado con cambios del equipo');
          }}
        }}
      }} catch(e) {{
        if (!silent) console.warn('Error al leer de la base de datos compartida:', e);
      }}
    }}

    async function saveToCloud() {{
      if (!isLiveSyncActive()) return;
      if (syncInFlight) return;
      syncInFlight = true;
      try {{
        await fetch(SYNC_URL, {{
          method: 'POST',
          mode: 'no-cors',
          headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
          body: JSON.stringify(STATE)
        }});
        syncInFlight = false;
        showToast('☁️ Cambios sincronizados con el equipo');
      }} catch(e) {{
        syncInFlight = false;
        console.warn('Error al guardar en la nube compartida:', e);
      }}
    }}

    function openSyncModal() {{
      document.getElementById('sync-url-input').value = SYNC_URL || '';
      openModal('sync-modal');
    }}

    function saveSyncUrl() {{
      const val = document.getElementById('sync-url-input').value.trim();
      SYNC_URL = val;
      localStorage.setItem(SYNC_URL_KEY, val);
      updateStorageBadge();
      closeModal('sync-modal');
      if (val) {{
        showToast('⚡ Conectando a la base de datos compartida...');
        loadFromCloud(false);
      }} else {{
        showToast('Modo desconectado (sólo memoria local)');
      }}
    }}

    async function testSyncConnection() {{
      const val = document.getElementById('sync-url-input').value.trim();
      if (!val) {{
        alert('Por favor pega una URL de Google Apps Script primero.');
        return;
      }}
      showToast('Probando conexión...');
      try {{
        const res = await fetch(val, {{ redirect: 'follow' }});
        const data = await res.json();
        if (data) {{
          alert('¡Conexión exitosa! La base de datos compartida está activa y respondiendo.');
        }}
      }} catch(err) {{
        alert('No se pudo conectar. Verifica que la implementación en Apps Script tenga acceso: "Cualquier persona" (Anyone).');
      }}
    }}

    function copyScriptCode() {{
      const code = `function doGet(e) {{
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var rawJson = sheet.getRange("A1").getValue();
  var responseData;
  try {{ responseData = rawJson ? JSON.parse(rawJson) : {{ posts: [], _selMonth: "2026-09" }}; }}
  catch(err) {{ responseData = {{ posts: [], _selMonth: "2026-09" }}; }}
  return ContentService.createTextOutput(JSON.stringify(responseData)).setMimeType(ContentService.MimeType.JSON);
}}

function doPost(e) {{
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var contents = e.postData ? e.postData.contents : "";
  if (contents) {{
    sheet.getRange("A1").setValue(contents);
    try {{
      var parsed = JSON.parse(contents);
      if (parsed && parsed.posts) updateSpreadsheetTable(sheet, parsed.posts);
    }} catch(err) {{}}
  }}
  return ContentService.createTextOutput(JSON.stringify({{ status: "success" }})).setMimeType(ContentService.MimeType.JSON);
}}

function updateSpreadsheetTable(sheet, posts) {{
  var lastRow = sheet.getLastRow();
  if (lastRow >= 3) sheet.getRange(3, 1, lastRow - 2, 8).clearContent();
  var headers = [["Fecha", "Día", "Formato", "Título / Tema", "Estado", "Obligatoria", "Hora / Notas", "ID"]];
  sheet.getRange("A3:H3").setValues(headers).setFontWeight("bold").setBackground("#ef6c1a").setFontColor("#ffffff");
  if (!posts || posts.length === 0) return;
  var DAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
  var statusLabels = {{ "pendiente": "⏳ Pendiente", "en_progreso": "🔄 En progreso", "listo": "✅ Listo", "no_realizado": "❌ No realizado" }};
  var rows = posts.map(function(p) {{
    var d = new Date(p.date + "T00:00:00");
    var dayName = isNaN(d.getTime()) ? "" : DAYS_ES[(d.getDay() + 6) % 7];
    return [p.date||"", dayName, p.type||"", p.title||"", statusLabels[p.status]||p.status||"", p.mandatory?"Sí":"No", (p.time?p.time+" | ":"")+(p.notes||""), p.id||""];
  }});
  sheet.getRange(4, 1, rows.length, 8).setValues(rows);
  sheet.autoResizeColumns(1, 8);
}}`;
      navigator.clipboard.writeText(code).then(() => {{
        showToast('📋 Código copiado. Pégalo en tu Google Apps Script.');
      }}).catch(() => {{
        alert('Abre el archivo codigo_google_sheets.js en tu carpeta para copiar el código.');
      }});
    }}

    // --- THEME SWITCHER ---
    function initTheme() {{
      const saved = localStorage.getItem(THEME_KEY);
      if (saved) {{
        document.documentElement.setAttribute('data-theme', saved);
      }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
        document.documentElement.setAttribute('data-theme', 'dark');
      }}
      updateThemeBtn();
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem(THEME_KEY, next);
      updateThemeBtn();
      showToast(next === 'dark' ? '🌙 Modo oscuro activado' : '☀️ Modo claro activado');
    }}

    function updateThemeBtn() {{
      const current = document.documentElement.getAttribute('data-theme');
      const btn = document.getElementById('theme-btn');
      if (btn) {{
        btn.innerHTML = current === 'dark' ? '☀️' : '🌙';
      }}
    }}

    // --- NAVIGATION & TABS ---
    let curTab = 'semana';
    let weekOffset = 0;
    const DAYS = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
    const TYPES = ['Reel','Carrusel','Post','Story'];
    const TYPE_ICONS = {{ Reel: '🎬', Carrusel: '🎠', Post: '🖼️', Story: '📱' }};
    const ICON = {{ pendiente:'⏳', en_progreso:'🔄', listo:'✅', no_realizado:'❌' }};
    const LABEL = {{ pendiente:'Pendiente', en_progreso:'En progreso', listo:'Listo', no_realizado:'No realizado' }};
    const STNEXT = {{ pendiente:'en_progreso', en_progreso:'listo', listo:'no_realizado', no_realizado:'pendiente' }};

    // Filter and search state
    let searchQuery = '';
    let filterType = 'all';
    let filterStatus = 'all';

    function setTab(t) {{
      curTab = t;
      document.querySelectorAll('.view-tab').forEach(el => el.classList.toggle('active', el.dataset.tab === t));
      document.getElementById('view-semana').style.display = t === 'semana' ? '' : 'none';
      document.getElementById('view-planner').style.display = t === 'planner' ? '' : 'none';
      document.getElementById('view-mes').style.display = t === 'mes' ? '' : 'none';
      render();
    }}

    // --- DATE HELPERS ---
    function mondayOf(d) {{
      const x = new Date(d);
      const day = (x.getDay() + 6) % 7;
      x.setDate(x.getDate() - day);
      x.setHours(0, 0, 0, 0);
      return x;
    }}
    function iso(d) {{ return d.toISOString().slice(0, 10); }}
    function fmt(d) {{ return d.toLocaleDateString('es-ES', {{ day: '2-digit', month: 'short' }}); }}
    function uid() {{ return 'p' + Math.random().toString(36).slice(2, 9); }}
    function todayIso() {{ return iso(new Date()); }}

    function weekDates(offset) {{
      const base = mondayOf(new Date());
      base.setDate(base.getDate() + offset * 7);
      return Array.from({{ length: 7 }}, (_, i) => {{
        const d = new Date(base);
        d.setDate(d.getDate() + i);
        return d;
      }});
    }}

    function monthKey(dateStr) {{ return dateStr.slice(0, 7); }}
    function monthLabel(mk) {{
      const [y, m] = mk.split('-').map(Number);
      return new Date(y, m - 1, 1).toLocaleDateString('es-ES', {{ month: 'long', year: 'numeric' }});
    }}

    function selectableMonths() {{
      const months = [...new Set(STATE.posts.map(p => monthKey(p.date)))].filter(Boolean).sort();
      const curMk = monthKey(todayIso());
      if (!months.includes(curMk)) months.push(curMk);
      months.sort();
      if (!STATE._selMonth || !months.includes(STATE._selMonth)) STATE._selMonth = curMk;
      return months;
    }}

    function monthWeeks(mk) {{
      const [y, m] = mk.split('-').map(Number);
      const first = new Date(y, m - 1, 1);
      const last = new Date(y, m, 0);
      let cur = mondayOf(first);
      const weeks = [];
      while (cur <= last) {{
        weeks.push(Array.from({{ length: 7 }}, (_, i) => {{
          const d = new Date(cur);
          d.setDate(d.getDate() + i);
          return d;
        }}));
        cur.setDate(cur.getDate() + 7);
      }}
      return weeks;
    }}

    function ensureMandatory(dates) {{
      let changed = false;
      dates.forEach(d => {{
        const key = iso(d);
        const exists = STATE.posts.some(p => p.date === key && p.mandatory);
        if (!exists) {{
          STATE.posts.push({{
            id: uid(),
            date: key,
            title: 'Historia diaria',
            type: 'Story',
            status: 'pendiente',
            mandatory: true
          }});
          changed = true;
        }}
      }});
      if (changed) saveToStorage();
      return changed;
    }}

    // --- FILTER & SEARCH LOGIC ---
    function filterPosts(postsList) {{
      return postsList.filter(p => {{
        if (filterType !== 'all' && p.type !== filterType) return false;
        if (filterStatus !== 'all' && p.status !== filterStatus) return false;
        if (searchQuery.trim() !== '') {{
          const q = searchQuery.toLowerCase();
          const matchTitle = (p.title || '').toLowerCase().includes(q);
          const matchNotes = (p.notes || '').toLowerCase().includes(q);
          const matchType = (p.type || '').toLowerCase().includes(q);
          if (!matchTitle && !matchNotes && !matchType) return false;
        }}
        return true;
      }});
    }}

    function handleSearch(val) {{
      searchQuery = val;
      updateFilterNotice();
      render();
    }}

    function handleFilterType(val) {{
      filterType = val;
      updateFilterNotice();
      render();
    }}

    function handleFilterStatus(val) {{
      filterStatus = val;
      updateFilterNotice();
      render();
    }}

    function quickFilterStatus(status) {{
      filterStatus = status;
      document.getElementById('filter-status').value = status;
      updateFilterNotice();
      render();
    }}

    function clearFilters() {{
      searchQuery = '';
      filterType = 'all';
      filterStatus = 'all';
      document.getElementById('search-input').value = '';
      document.getElementById('filter-type').value = 'all';
      document.getElementById('filter-status').value = 'all';
      updateFilterNotice();
      render();
    }}

    function updateFilterNotice() {{
      const notice = document.getElementById('filter-notice');
      const isFiltered = searchQuery !== '' || filterType !== 'all' || filterStatus !== 'all';
      notice.style.display = isFiltered ? 'inline-block' : 'none';

      document.querySelectorAll('.stat-badge').forEach(el => el.classList.remove('filter-active'));
      if (filterStatus === 'all') document.getElementById('qf-all')?.classList.add('filter-active');
      else if (filterStatus === 'listo') document.getElementById('qf-listo')?.classList.add('filter-active');
      else if (filterStatus === 'en_progreso') document.getElementById('qf-prog')?.classList.add('filter-active');
      else if (filterStatus === 'pendiente') document.getElementById('qf-pend')?.classList.add('filter-active');
      else if (filterStatus === 'no_realizado') document.getElementById('qf-fail')?.classList.add('filter-active');
    }}

    function updateQuickCounts() {{
      const total = STATE.posts.length;
      const listo = STATE.posts.filter(p => p.status === 'listo').length;
      const prog = STATE.posts.filter(p => p.status === 'en_progreso').length;
      const pend = STATE.posts.filter(p => p.status === 'pendiente').length;
      const fail = STATE.posts.filter(p => p.status === 'no_realizado').length;

      document.getElementById('count-total').textContent = total;
      document.getElementById('count-listo').textContent = listo;
      document.getElementById('count-prog').textContent = prog;
      document.getElementById('count-pend').textContent = pend;
      document.getElementById('count-fail').textContent = fail;
    }}

    // --- RENDER SEMANA (WEEK VIEW) ---
    function renderSemana() {{
      const dates = weekDates(weekOffset);
      if (ensureMandatory(dates)) {{
        renderSemana();
        return;
      }}

      const el = document.getElementById('view-semana');
      const label = `${{fmt(dates[0])}} – ${{fmt(dates[6])}} (${{dates[0].getFullYear()}})`;
      const tIso = todayIso();

      let html = `
        <div class="weeknav-container">
          <div class="weeknav-controls">
            <button class="nav-btn" onclick="weekOffset--; renderSemana()">‹ Anterior</button>
            <span class="week-label">${{label}}</span>
            <button class="nav-btn" onclick="weekOffset++; renderSemana()">Siguiente ›</button>
            ${{weekOffset !== 0 ? `<button class="nav-btn" onclick="weekOffset=0; renderSemana()">Esta semana</button>` : `<span class="today-pill">Semana actual</span>`}}
          </div>
          <div>
            <button class="btn btn-secondary" onclick="openNewPostModal('${{iso(dates[0])}}')">
              <span>+</span> Nueva publicación
            </button>
          </div>
        </div>
        <div class="grid-week">
      `;

      dates.forEach((d, i) => {{
        const key = iso(d);
        const allDayPosts = STATE.posts.filter(p => p.date === key).sort((a,b) => (b.mandatory ? 1 : 0) - (a.mandatory ? 1 : 0));
        const filteredPosts = filterPosts(allDayPosts);
        const isToday = key === tIso;

        html += `
          <div class="day-col ${{isToday ? 'is-today' : ''}}">
            <div class="day-col-header">
              <div class="day-name-block">
                <span class="day-name">${{DAYS[i]}}</span>
                <span class="day-number">${{d.getDate()}}</span>
              </div>
              <span class="day-count-badge" title="${{allDayPosts.length}} planificadas">${{filteredPosts.length}}/${{allDayPosts.length}}</span>
            </div>
            
            <div class="posts-container">
        `;

        if (filteredPosts.length === 0) {{
          html += `
            <div style="font-size:12px; color:var(--ink-muted); text-align:center; padding:18px 0; border:1px dashed var(--card-border); border-radius:var(--radius-md);">
              ${{allDayPosts.length > 0 ? 'Filtrado' : 'Sin piezas'}}
            </div>
          `;
        }}

        filteredPosts.forEach(p => {{
          const typeIcon = TYPE_ICONS[p.type] || '📌';
          const lockCtl = p.mandatory
            ? '<span title="Tarea diaria obligatoria" style="font-size:12px;">🔒</span>'
            : `<span class="action-icon" onclick="event.stopPropagation(); deletePost('${{p.id}}')" title="Eliminar">✕</span>`;

          html += `
            <div class="post-card" onclick="cycleStatus('${{p.id}}')" title="Clic para cambiar estado rápido">
              <div class="post-card-top">
                <span class="type-badge type-${{p.type}}">${{typeIcon}} ${{p.type}}</span>
                <div class="post-card-actions">
                  <span class="action-icon" onclick="event.stopPropagation(); openEditPostModal('${{p.id}}')" title="Editar publicación">✏️</span>
                  ${{lockCtl}}
                </div>
              </div>
              <div class="post-title">${{escapeHtml(p.title)}}</div>
              ${{p.time ? `<div class="post-notes">⏰ ${{escapeHtml(p.time)}}</div>` : ''}}
              ${{p.notes ? `<div class="post-notes">📝 ${{escapeHtml(p.notes)}}</div>` : ''}}
              <div style="margin-top:2px;">
                <span class="status-pill st-${{p.status}}" onclick="event.stopPropagation(); cycleStatus('${{p.id}}')">
                  ${{ICON[p.status]}} ${{LABEL[p.status]}}
                </span>
              </div>
            </div>
          `;
        }});

        html += `
            </div>
            <button class="btn-add-day" onclick="openNewPostModal('${{key}}')">
              <span>+</span> Agregar
            </button>
          </div>
        `;
      }});

      html += '</div>';
      el.innerHTML = html;
    }}

    // --- RENDER PLANNER (MONTH GRID VIEW) ---
    function renderPlanner() {{
      const el = document.getElementById('view-planner');
      const months = selectableMonths();
      const weeks = monthWeeks(STATE._selMonth);
      const inMonthDates = weeks.flat().filter(d => monthKey(iso(d)) === STATE._selMonth);
      if (ensureMandatory(inMonthDates)) {{
        renderPlanner();
        return;
      }}

      const currentIdx = months.indexOf(STATE._selMonth);
      const prevMonth = currentIdx > 0 ? months[currentIdx - 1] : null;
      const nextMonth = currentIdx < months.length - 1 ? months[currentIdx + 1] : null;

      let html = `
        <div class="month-header-row">
          <div class="month-selector-group">
            <button class="nav-btn" ${{prevMonth ? `onclick="STATE._selMonth='${{prevMonth}}'; renderPlanner()"` : 'disabled'}} style="opacity:${{prevMonth?1:0.4}}">‹</button>
            <select onchange="STATE._selMonth=this.value; renderPlanner()">
              ${{months.map(m => `<option value="${{m}}" ${{m === STATE._selMonth ? 'selected' : ''}}>${{monthLabel(m).replace(/^\\w/, c => c.toUpperCase())}}</option>`).join('')}}
            </select>
            <button class="nav-btn" ${{nextMonth ? `onclick="STATE._selMonth='${{nextMonth}}'; renderPlanner()"` : 'disabled'}} style="opacity:${{nextMonth?1:0.4}}">›</button>
          </div>
          <div>
            <button class="btn btn-secondary" onclick="openNewPostModal('${{STATE._selMonth}}-01')">
              <span>+</span> Nueva publicación en este mes
            </button>
          </div>
        </div>

        <div class="planner-weekdays-row">
          ${{DAYS.map(d => `<div>${{d}}</div>`).join('')}}
        </div>
        <div class="planner-calendar-grid">
      `;

      const tIso = todayIso();
      weeks.forEach(week => {{
        week.forEach((d, idx) => {{
          const key = iso(d);
          const inMonth = monthKey(key) === STATE._selMonth;
          const isToday = key === tIso;
          const allDayPosts = STATE.posts.filter(p => p.date === key).sort((a,b) => (b.mandatory ? 1 : 0) - (a.mandatory ? 1 : 0));
          const filteredPosts = filterPosts(allDayPosts);

          html += `
            <div class="planner-cell ${{inMonth ? '' : 'dim'}} ${{isToday ? 'is-today' : ''}}">
              <div class="planner-cell-header">
                <span class="planner-day-num">${{d.getDate()}}</span>
                <span class="planner-add-mini" onclick="openNewPostModal('${{key}}')" title="Agregar pieza este día">+</span>
              </div>
              <div class="planner-chips-list">
          `;

          filteredPosts.forEach(p => {{
            const typeIcon = TYPE_ICONS[p.type] || '📌';
            const lock = p.mandatory ? ' 🔒' : '';
            html += `
              <div class="planner-chip st-${{p.status}}" onclick="cycleStatus('${{p.id}}')" title="${{escapeHtml(p.title)}} • ${{p.type}} (${{LABEL[p.status]}})">
                <span>${{typeIcon}}</span>
                <span class="planner-chip-title">${{escapeHtml(p.title)}}${{lock}}</span>
              </div>
            `;
          }});

          html += `
              </div>
            </div>
          `;
        }});
      }});

      html += `</div>`;
      el.innerHTML = html;
    }}

    // --- RENDER DESGLOSE & MÉTRICAS (DASHBOARD) ---
    function renderMes() {{
      const el = document.getElementById('view-mes');
      const months = selectableMonths();

      const postsInMonth = STATE.posts.filter(p => monthKey(p.date) === STATE._selMonth);
      const filteredPosts = filterPosts(postsInMonth);

      const total = postsInMonth.length;
      const listos = postsInMonth.filter(p => p.status === 'listo').length;
      const prog = postsInMonth.filter(p => p.status === 'en_progreso').length;
      const pend = postsInMonth.filter(p => p.status === 'pendiente').length;
      const fail = postsInMonth.filter(p => p.status === 'no_realizado').length;

      const pctListo = total > 0 ? Math.round((listos / total) * 100) : 0;
      const pctProg = total > 0 ? Math.round((prog / total) * 100) : 0;
      const pctPend = total > 0 ? Math.round((pend / total) * 100) : 0;
      const pctFail = total > 0 ? Math.round((fail / total) * 100) : 0;

      let html = `
        <div class="month-header-row">
          <div class="month-selector-group">
            <select onchange="STATE._selMonth=this.value; renderMes()">
              ${{months.map(m => `<option value="${{m}}" ${{m === STATE._selMonth ? 'selected' : ''}}>${{monthLabel(m).replace(/^\\w/, c => c.toUpperCase())}}</option>`).join('')}}
            </select>
          </div>
          <div>
            <button class="btn btn-secondary" onclick="exportExcel()">
              <span>📊</span> Exportar este mes a Excel
            </button>
          </div>
        </div>

        <!-- Metrics Cards -->
        <div class="dashboard-metrics-grid">
          <div class="metric-card m-total">
            <div class="metric-num">${{total}}</div>
            <div class="metric-label">Total Publicaciones</div>
          </div>
          <div class="metric-card m-listo">
            <div class="metric-num" style="color:var(--green)">✅ ${{listos}}</div>
            <div class="metric-label">Listos / Publicados (${{pctListo}}%)</div>
          </div>
          <div class="metric-card m-prog">
            <div class="metric-num" style="color:#2563eb">🔄 ${{prog}}</div>
            <div class="metric-label">En Progreso (${{pctProg}}%)</div>
          </div>
          <div class="metric-card m-pend">
            <div class="metric-num" style="color:#e0901e">⏳ ${{pend}}</div>
            <div class="metric-label">Pendientes (${{pctPend}}%)</div>
          </div>
          <div class="metric-card m-fail">
            <div class="metric-num" style="color:#dc2626">❌ ${{fail}}</div>
            <div class="metric-label">No Realizados (${{pctFail}}%)</div>
          </div>
        </div>

        <!-- Visual Progress Bar -->
        <div class="progress-bar-container">
          <div class="progress-bar-info">
            <span>Tasa de Cumplimiento Global del Mes</span>
            <span style="color:var(--green); font-size:16px;">${{pctListo}}% Completado</span>
          </div>
          <div class="progress-track" title="Verde: Listo, Azul: En progreso, Amarillo: Pendiente, Rojo: No realizado">
            <div class="progress-fill-listo" style="width: ${{pctListo}}%"></div>
            <div class="progress-fill-prog" style="width: ${{pctProg}}%"></div>
            <div class="progress-fill-pend" style="width: ${{pctPend}}%"></div>
            <div class="progress-fill-fail" style="width: ${{pctFail}}%"></div>
          </div>
        </div>
      `;

      // Group table by weeks
      const byWeek = {{}};
      filteredPosts.forEach(p => {{
        const wk = iso(mondayOf(new Date(p.date)));
        (byWeek[wk] = byWeek[wk] || []).push(p);
      }});
      const weeks = Object.keys(byWeek).sort();

      if (weeks.length === 0) {{
        html += `
          <div class="table-container" style="padding:32px; text-align:center; color:var(--ink-muted);">
            No hay publicaciones que coincidan con la búsqueda o filtro en este mes.
          </div>
        `;
      }} else {{
        html += `
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Semana</th>
                  <th>Fecha</th>
                  <th>Formato</th>
                  <th>Título / Tema</th>
                  <th>Estado</th>
                  <th style="text-align:right;">Acciones</th>
                </tr>
              </thead>
              <tbody>
        `;

        weeks.forEach(wk => {{
          const wd = new Date(wk);
          const wEnd = new Date(wk);
          wEnd.setDate(wEnd.getDate() + 6);
          const items = byWeek[wk].sort((a,b) => a.date.localeCompare(b.date));

          items.forEach((p, idx) => {{
            const typeIcon = TYPE_ICONS[p.type] || '📌';
            html += `
              <tr>
                <td style="font-weight:600; color:var(--ink-soft);">${{idx === 0 ? `${{fmt(wd)}} – ${{fmt(wEnd)}}` : ''}}</td>
                <td style="font-family:var(--font-mono); font-weight:600;">${{fmt(new Date(p.date))}}</td>
                <td><span class="type-badge type-${{p.type}}">${{typeIcon}} ${{p.type}}</span></td>
                <td style="font-weight:600;">
                  ${{escapeHtml(p.title)}}
                  ${{p.mandatory ? ' <span style="font-size:11px; color:var(--orange); font-weight:700;">🔒 Obligatoria</span>' : ''}}
                  ${{p.notes ? `<div style="font-size:11px; color:var(--ink-muted); font-weight:normal;">${{escapeHtml(p.notes)}}</div>` : ''}}
                </td>
                <td>
                  <span class="status-pill st-${{p.status}}" onclick="cycleStatus('${{p.id}}')" style="cursor:pointer;" title="Clic para avanzar estado">
                    ${{ICON[p.status]}} ${{LABEL[p.status]}}
                  </span>
                </td>
                <td style="text-align:right;">
                  <button class="btn btn-secondary btn-icon" style="padding:4px 8px; font-size:12px;" onclick="openEditPostModal('${{p.id}}')">✏️</button>
                  ${{!p.mandatory ? `<button class="btn btn-secondary btn-icon" style="padding:4px 8px; font-size:12px; margin-left:4px;" onclick="deletePost('${{p.id}}')">✕</button>` : ''}}
                </td>
              </tr>
            `;
          }});
        }});

        html += `
              </tbody>
            </table>
          </div>
        `;
      }}

      el.innerHTML = html;
    }}

    function render() {{
      updateQuickCounts();
      updateStorageBadge();
      if (curTab === 'semana') renderSemana();
      else if (curTab === 'planner') renderPlanner();
      else renderMes();
    }}

    // --- ACTIONS ON POSTS ---
    function cycleStatus(id) {{
      const p = STATE.posts.find(x => x.id === id);
      if (!p) return;
      p.status = STNEXT[p.status] || 'pendiente';
      saveToStorage();
      render();
      showToast(`Estado cambiado a: ${{LABEL[p.status]}}`);
      saveToCloud();
    }}

    function deletePost(id) {{
      const p = STATE.posts.find(x => x.id === id);
      if (!p) return;
      if (p.mandatory) {{
        alert('Esta es una historia diaria obligatoria generada automáticamente.');
        return;
      }}
      if (confirm(`¿Eliminar "${{p.title}}"?`)) {{
        STATE.posts = STATE.posts.filter(x => x.id !== id);
        saveToStorage();
        render();
        showToast('🗑️ Publicación eliminada');
        saveToCloud();
      }}
    }}

    // --- MODAL LOGIC (ADD / EDIT) ---
    function openNewPostModal(defaultDate) {{
      document.getElementById('modal-title').textContent = 'Nueva Publicación';
      document.getElementById('form-post-id').value = '';
      document.getElementById('form-date').value = defaultDate || todayIso();
      document.getElementById('form-type').value = 'Reel';
      document.getElementById('form-title').value = '';
      document.getElementById('form-status').value = 'pendiente';
      document.getElementById('form-time').value = '';
      document.getElementById('form-notes').value = '';
      openModal('post-modal');
      setTimeout(() => document.getElementById('form-title').focus(), 100);
    }}

    function openEditPostModal(id) {{
      const p = STATE.posts.find(x => x.id === id);
      if (!p) return;
      document.getElementById('modal-title').textContent = 'Editar Publicación';
      document.getElementById('form-post-id').value = p.id;
      document.getElementById('form-date').value = p.date;
      document.getElementById('form-type').value = p.type;
      document.getElementById('form-title').value = p.title;
      document.getElementById('form-status').value = p.status;
      document.getElementById('form-time').value = p.time || '';
      document.getElementById('form-notes').value = p.notes || '';
      openModal('post-modal');
      setTimeout(() => document.getElementById('form-title').focus(), 100);
    }}

    function submitPostModal() {{
      const id = document.getElementById('form-post-id').value;
      const date = document.getElementById('form-date').value;
      const type = document.getElementById('form-type').value;
      const title = document.getElementById('form-title').value.trim();
      const status = document.getElementById('form-status').value;
      const time = document.getElementById('form-time').value.trim();
      const notes = document.getElementById('form-notes').value.trim();

      if (!title) {{
        alert('Por favor escribe un título o tema para la publicación.');
        return;
      }}

      if (id) {{
        // Edit existing
        const p = STATE.posts.find(x => x.id === id);
        if (p) {{
          p.date = date;
          p.type = type;
          p.title = title;
          p.status = status;
          p.time = time;
          p.notes = notes;
          showToast('✅ Publicación actualizada');
        }}
      }} else {{
        // New post
        STATE.posts.push({{
          id: uid(),
          date,
          type,
          title,
          status,
          time,
          notes,
          mandatory: false
        }});
        showToast('✨ Nueva publicación agregada');
      }}

      saveToStorage();
      closeModal('post-modal');
      render();
      saveToCloud();
    }}

    function openModal(id) {{
      document.getElementById(id).classList.add('active');
    }}

    function closeModal(id) {{
      document.getElementById(id).classList.remove('active');
    }}

    function handleBackdropClick(e, id) {{
      if (e.target.id === id) closeModal(id);
    }}

    function openShareModal() {{
      openModal('share-modal');
    }}

    // --- DATA SAVING & SHARING ---
    async function saveHtmlFile() {{
      const fullHtml = generateSelfUpdatingHtml();
      const blob = new Blob([fullHtml], {{ type: 'text/html;charset=utf-8' }});
      const filename = 'calendario-ig-standalone.html';

      if (window.showSaveFilePicker) {{
        try {{
          const handle = await window.showSaveFilePicker({{
            suggestedName: filename,
            types: [{{
              description: 'Archivo HTML autónomo',
              accept: {{ 'text/html': ['.html'] }}
            }}]
          }});
          const writable = await handle.createWritable();
          await writable.write(blob);
          await writable.close();
          showToast('💾 ¡Archivo HTML guardado con éxito! Listo para compartir.');
          return;
        }} catch(err) {{
          if (err.name === 'AbortError') return;
          console.warn('showSaveFilePicker falló, usando descarga estándar:', err);
        }}
      }}

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      showToast('💾 Archivo HTML descargado con todas tus modificaciones.');
    }}

    function generateSelfUpdatingHtml() {{
      let markup = document.documentElement.outerHTML;
      const jsonString = JSON.stringify(STATE);
      markup = markup.replace(
        /<script id="data" type="application\\/json">[\\s\\S]*?<\\/script>/,
        `<script id="data" type="application/json">${{jsonString}}<\\/script>`
      );
      // Embed current SYNC_URL so any recipient automatically connects
      markup = markup.replace(
        /let EMBEDDED_SYNC_URL = '.*?';/,
        `let EMBEDDED_SYNC_URL = '${{SYNC_URL}}';`
      );
      return '<!doctype html>\\n<html lang="es">\\n' + markup.slice(markup.indexOf('<head>'));
    }}

    function copyShareableUrl() {{
      try {{
        const jsonStr = JSON.stringify(STATE);
        const encoded = encodeURIComponent(jsonStr);
        const shareUrl = window.location.origin + window.location.pathname + '#data=' + encoded;
        navigator.clipboard.writeText(shareUrl).then(() => {{
          showToast('📋 ¡Enlace copiado! Quien lo abra verá este calendario.');
        }}).catch(() => {{
          prompt('Copia este enlace para compartir:', shareUrl);
        }});
      }} catch(e) {{
        console.error(e);
        alert('No se pudo generar el enlace. Utiliza la opción de Guardar Archivo HTML.');
      }}
    }}

    function exportJsonBackup() {{
      const blob = new Blob([JSON.stringify(STATE, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `calendario-umwelt-respaldo-${{todayIso()}}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      showToast('📥 Respaldo JSON descargado');
    }}

    function triggerImportJson() {{
      document.getElementById('json-file-input').click();
    }}

    function importJsonFile(e) {{
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(evt) {{
        try {{
          const parsed = JSON.parse(evt.target.result);
          if (parsed && Array.isArray(parsed.posts)) {{
            STATE = parsed;
            saveToStorage();
            render();
            closeModal('share-modal');
            showToast(`✅ Se importaron ${{STATE.posts.length}} publicaciones con éxito.`);
            saveToCloud();
          }} else {{
            alert('El archivo no contiene un formato de calendario válido.');
          }}
        }} catch(err) {{
          alert('Error al leer el archivo JSON.');
        }}
      }};
      reader.readAsText(file);
      e.target.value = '';
    }}

    function resetToInitialData() {{
      if (confirm('¿Restablecer el calendario a la plantilla inicial? Se borrarán las modificaciones locales no guardadas en archivo.')) {{
        localStorage.removeItem(STORAGE_KEY);
        try {{
          const embedded = JSON.parse(document.getElementById('data').textContent);
          STATE = embedded;
          saveToStorage();
          render();
          closeModal('share-modal');
          showToast('🔄 Calendario restablecido');
        }} catch(e) {{
          location.reload();
        }}
      }}
    }}

    // --- EXPORT TO EXCEL ---
    function exportExcel() {{
      if (typeof XLSX === 'undefined') {{
        alert('Cargando librería de Excel, por favor intenta en un segundo.');
        return;
      }}
      const rows = STATE.posts.slice().sort((a,b) => a.date.localeCompare(b.date)).map(p => {{
        const d = new Date(p.date);
        return {{
          'Fecha': p.date,
          'Día': DAYS[(d.getDay() + 6) % 7],
          'Mes': monthLabel(monthKey(p.date)).replace(/^\\w/, c => c.toUpperCase()),
          'Título': p.title,
          'Tipo': p.type,
          'Estado': LABEL[p.status] || p.status,
          'Hora': p.time || '',
          'Notas': p.notes || '',
          'Obligatoria': p.mandatory ? 'Sí' : 'No'
        }};
      }});

      const ws = XLSX.utils.json_to_sheet(rows);
      ws['!cols'] = [
        {{ wch: 12 }}, {{ wch: 12 }}, {{ wch: 16 }}, {{ wch: 36 }},
        {{ wch: 12 }}, {{ wch: 14 }}, {{ wch: 14 }}, {{ wch: 30 }}, {{ wch: 12 }}
      ];
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Calendario RRSS');
      XLSX.writeFile(wb, `calendario-rrss-umwelt-${{todayIso()}}.xlsx`);
      showToast('📊 Archivo Excel generado y descargado');
    }}

    // --- TOAST NOTIFICATIONS ---
    function showToast(msg) {{
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = msg;
      container.appendChild(toast);
      setTimeout(() => {{
        toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 350);
      }}, 3200);
    }}

    function escapeHtml(s) {{
      if (!s) return '';
      const d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }}

    // --- INITIALIZATION ---
    window.addEventListener('DOMContentLoaded', () => {{
      initTheme();
      initState();
      render();

      // Check if team sync is configured and fetch latest updates
      if (isLiveSyncActive()) {{
        loadFromCloud(true);
        // Periodic background poll every 12s so other people's edits appear automatically
        setInterval(() => {{
          // Only sync if user is not actively typing in an input
          const activeTag = document.activeElement ? document.activeElement.tagName : '';
          if (activeTag !== 'INPUT' && activeTag !== 'TEXTAREA') {{
            loadFromCloud(true);
          }}
        }}, 12000);
      }}
    }});
  </script>
</body>
</html>'''

with open('calendario-ig-standalone.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Updated calendario-ig-standalone.html with live team synchronization!')
