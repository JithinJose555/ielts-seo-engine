$ErrorActionPreference = "Stop"
$InputDir = $PSScriptRoot
$OutputDir = Join-Path $InputDir "dist"

if (-not (Test-Path -Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$TemplatePath = Join-Path $InputDir "template.html"
$DataPath = Join-Path $InputDir "data.csv"

if (-not (Test-Path -Path $TemplatePath) -or -not (Test-Path -Path $DataPath)) {
    Write-Host "Error: template.html or data.csv not found!"
    exit 1
}

$TemplateContent = Get-Content -Path $TemplatePath -Raw -Encoding UTF8
$Data = Import-Csv $DataPath

$GeneratedCount = 0
$Pages = @()

foreach ($Row in $Data) {
    $Keyword = $Row.keyword.Trim()
    if ([string]::IsNullOrWhiteSpace($Keyword)) { continue }

    $ProblemName = $Row.problem_name.Trim()
    $Band5Example = $Row.band_5_example.Trim()
    $Band9Fix = $Row.band_9_fix.Trim()

    # Create slug
    $Slug = $Keyword.ToLower() -replace '[^a-z0-9\s-]', '' -replace '[\s\-]+', '-'
    $Slug = $Slug.Trim('-')
    
    $OutputFile = Join-Path $OutputDir "$Slug.html"

    # Replace placeholders
    $HtmlContent = $TemplateContent.Replace('{{keyword}}', $Keyword)
    $HtmlContent = $HtmlContent.Replace('{{problem_name}}', $ProblemName)
    $HtmlContent = $HtmlContent.Replace('{{band_5_example}}', $Band5Example)
    $HtmlContent = $HtmlContent.Replace('{{band_9_fix}}', $Band9Fix)

    Set-Content -Path $OutputFile -Value $HtmlContent -Encoding UTF8
    
    Write-Host "Generated: $OutputFile"
    $GeneratedCount++
    $Pages += [PSCustomObject]@{ Title = $Keyword; Url = "$Slug.html" }
}

# Generate index.html to prevent 404
$IndexLinkHtml = ""
foreach ($Page in $Pages) {
    $IndexLinkHtml += "<li><a href='$($Page.Url)'>$($Page.Title)</a></li>"
}

$IndexHtml = @"
<!DOCTYPE html>
<html>
<head><title>IELTS Surgical Logic - All Fixes</title></head>
<body>
    <h1>IELTS Surgical Logic: Master Directory</h1>
    <ul>$IndexLinkHtml</ul>
</body>
</html>
"@

Set-Content -Path (Join-Path $OutputDir "index.html") -Value $IndexHtml -Encoding UTF8

Write-Host "`n✅ Engine completed successfully! $GeneratedCount optimized SEO pages and index.html generated in the 'dist' folder."
