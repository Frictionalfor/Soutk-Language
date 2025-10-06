# Comprehensive test script to run ALL .stk files and provide feedback

Write-Host "🧙‍♂️ COMPREHENSIVE SOUTK LANGUAGE TEST 🧙‍♂️" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Get all .stk files
$stkFiles = Get-ChildItem -Path . -Filter "*.stk" -Recurse | Sort-Object FullName

$totalFiles = $stkFiles.Count
$successCount = 0
$errorCount = 0
$results = @()

Write-Host "Found $totalFiles .stk files to test" -ForegroundColor Yellow
Write-Host ""

foreach ($file in $stkFiles) {
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
    Write-Host "Testing: $relativePath" -ForegroundColor White
    
    try {
        # Run the file with the new interpreter
        $output = & python "src/soutk_interpreter.py" $file.FullName 2>&1
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0 -and $output -notmatch "❌|💥") {
            Write-Host "  ✅ SUCCESS" -ForegroundColor Green
            $successCount++
            $results += [PSCustomObject]@{
                File = $relativePath
                Status = "SUCCESS"
                Output = $output -join "`n"
            }
        } else {
            Write-Host "  ❌ FAILED" -ForegroundColor Red
            $errorCount++
            $results += [PSCustomObject]@{
                File = $relativePath
                Status = "FAILED"
                Output = $output -join "`n"
            }
        }
    } catch {
        Write-Host "  💥 ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
        $results += [PSCustomObject]@{
            File = $relativePath
            Status = "ERROR"
            Output = $_.Exception.Message
        }
    }
}

Write-Host ""
Write-Host "🎯 FINAL RESULTS:" -ForegroundColor Cyan
Write-Host "=" * 30 -ForegroundColor Cyan
Write-Host "Total Files: $totalFiles" -ForegroundColor White
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $errorCount" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($successCount / $totalFiles) * 100, 2))%" -ForegroundColor Yellow

if ($errorCount -gt 0) {
    Write-Host ""
    Write-Host "❌ FAILED FILES:" -ForegroundColor Red
    $failedFiles = $results | Where-Object { $_.Status -ne "SUCCESS" }
    foreach ($failed in $failedFiles) {
        Write-Host "  - $($failed.File)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🧙‍♂️ SOUTK Language Test Complete! 🧙‍♂️" -ForegroundColor Cyan