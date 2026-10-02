# make_pdf.ps1 — builds the FM & SM master book and exports CA_Inter_FMSM_Master_Book.pdf
# Usage:  .\make_pdf.ps1            (two export passes so the printed index page numbers settle)
#         .\make_pdf.ps1 -Passes 1  (quick draft; index numbers may be one page out)
# Notes:  Word's own "create bookmarks" export hangs on a large document, so Word exports a plain
#         PDF and sources\add_bookmarks.py adds the outline; sources\link_index.py makes the
#         index lines clickable. Run it in a normal PowerShell window (Word automation can
#         deadlock when started from a hidden child process).
param([int]$Passes = 2)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location $root
New-Item -ItemType Directory -Force (Join-Path $root 'build') | Out-Null
$docx = Join-Path $root 'build\CA_Inter_FMSM_Master_Book.docx'
$env:PYTHONIOENCODING = 'utf-8'

for ($i = 1; $i -le $Passes; $i++) {
    Write-Host "== pass $i of $Passes"
    Remove-Item $docx -Force -ErrorAction SilentlyContinue
    $env:HW_NO_UPDATEFIELDS = '1'; $env:HW_STATIC_TOC = '1'
    node book\build_fmsm_book.js book $docx
    if (-not (Test-Path $docx)) { throw 'docx build failed' }
    $raw = Join-Path $root 'build\raw.pdf'
    Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -Confirm:$false
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false; $w.DisplayAlerts = 0
    try {
        $d = $w.Documents.Open($docx, $false, $true, $false)
        # plain export: PDF=17, no open after export, print quality, whole document, no bookmarks, no tags
        $d.ExportAsFixedFormat($raw, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0, $false, $true, $false)
        $d.Close(0)
    } finally { try { $w.Quit() } catch {}; Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -Confirm:$false }
    python sources\add_bookmarks.py $raw build\new.pdf
    python sources\make_page_map.py build\new.pdf     # page numbers for the next pass's index
}
python sources\link_index.py build\new.pdf build\final.pdf
python sources\scan_pdf.py build\final.pdf
$out = Join-Path $root 'CA_Inter_FMSM_Master_Book.pdf'
try { Copy-Item build\final.pdf $out -Force } catch {
    $out = Join-Path $root ('CA_Inter_FMSM_Master_Book_' + (Get-Date -Format 'HHmm') + '.pdf')
    Copy-Item build\final.pdf $out -Force
    Write-Host 'The usual file was locked (open in a viewer?), so the book was saved under a new name.'
}
"Done: $out"
