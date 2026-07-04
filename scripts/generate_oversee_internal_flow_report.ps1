$ErrorActionPreference = "Continue"

$ReportDir = ".\outputs\reports"
$ReportPath = ".\outputs\reports\oversee_internal_flow_report.md"

New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

"# OVERSEE Internal Flow Inspection Report" | Set-Content $ReportPath
"" | Add-Content $ReportPath
"Generated at: $(Get-Date)" | Add-Content $ReportPath
"Repository root: $(Get-Location)" | Add-Content $ReportPath

function Add-Title($title) {
    "" | Add-Content $ReportPath
    "## $title" | Add-Content $ReportPath
    "" | Add-Content $ReportPath
    '```text' | Add-Content $ReportPath
}

function Add-End {
    '```' | Add-Content $ReportPath
}

function Run-And-Append($title, $command) {
    Add-Title $title
    try {
        Invoke-Expression $command | Out-String -Width 300 | Add-Content $ReportPath
    }
    catch {
        "ERROR: $($_.Exception.Message)" | Add-Content $ReportPath
    }
    Add-End
}

Run-And-Append "1. Top-level repository structure" "Get-ChildItem -Force | Select-Object Mode,Length,LastWriteTime,Name | Format-Table -AutoSize"

Run-And-Append "2. outputs structure" "Get-ChildItem -Recurse .\outputs -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize"

Run-And-Append "3. JSON files" "Get-ChildItem -Recurse -Filter *.json -File -ErrorAction SilentlyContinue | Where-Object { `$_.FullName -notmatch '\\.git\\|\\.venv\\|\\venv\\|\\__pycache__\\' } | Select-Object FullName,Length,LastWriteTime | Sort-Object FullName | Format-Table -AutoSize"

Run-And-Append "4. Markdown files" "Get-ChildItem -Recurse -Filter *.md -File -ErrorAction SilentlyContinue | Where-Object { `$_.FullName -notmatch '\\.git\\|\\.venv\\|\\venv\\|\\__pycache__\\' } | Select-Object FullName,Length,LastWriteTime | Sort-Object FullName | Format-Table -AutoSize"

$patterns = @(
    "COMP-001|COMP-002|compressor|bearing",
    "evidence_package|Evidence Package|validated evidence|evidence package",
    "canonical_context|Canonical Context|canonical decision state|CanonicalContext",
    "contextualized|contextualized_state|Contextualized|business interpretation|operational impact|feasibility|urgency",
    "case-managed|case_managed|case_state|blocker|blockers|readiness|ready|escalated|milestone|owner",
    "recommendation_record|recommendation package|recommendation_package|governed recommendation|recommendation rationale|execution mode",
    "protected_fact|protected facts|generative|deterministic comparison|fallback|schema validation|human review",
    "Layer 1|Layer 2|Layer 3|Layer 4|Layer 5|layer1|layer2|layer3|layer4|layer5",
    "traceability|provenance|source identifier|timestamp|audit|auditability"
)

$i = 5
foreach ($pattern in $patterns) {
    Add-Title "$i. Search pattern: $pattern"
    Get-ChildItem -Recurse -Include *.py,*.md,*.json,*.csv,*.yaml,*.yml,*.txt -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "\\.git\\|\\.venv\\|\\venv\\|\\__pycache__\\" } |
        Select-String -Pattern $pattern -CaseSensitive:$false |
        Select-Object Path,LineNumber,Line |
        Format-Table -AutoSize |
        Out-String -Width 300 |
        Add-Content $ReportPath
    Add-End
    $i++
}

Add-Title "Recent output file previews"
$recentFiles = Get-ChildItem -Recurse .\outputs -Include *.json,*.md,*.txt -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 20

foreach ($file in $recentFiles) {
    "----- $($file.FullName) -----" | Add-Content $ReportPath
    Get-Content $file.FullName -TotalCount 80 -ErrorAction SilentlyContinue | Add-Content $ReportPath
    "" | Add-Content $ReportPath
}
Add-End

"" | Add-Content $ReportPath
"# End of report" | Add-Content $ReportPath

Write-Host "Report generated:"
Write-Host (Resolve-Path $ReportPath)

Remove-Item $MyInvocation.MyCommand.Path -Force