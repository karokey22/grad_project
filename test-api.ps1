# test_api.ps1

$baseUrl = "http://127.0.0.1:5001"

$testCases = @(
    @{
        text = "The server is down and all systems are offline!"
        description = "IT Emergency"
    },
    @{
        text = "Need to update my direct deposit information"
        description = "Finance Request"
    },
    @{
        text = "Everything is working perfectly after the update"
        description = "Positive Feedback"
    }
)

foreach ($test in $testCases) {
    $body = @{
        text = $test.text
    } | ConvertTo-Json

    Write-Host "`nTesting with: $($test.description)" -ForegroundColor Cyan
    Write-Host "Text: $($test.text)" -ForegroundColor Gray

    # Test Department Prediction
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/predict_department" -Method Post -Body $body -ContentType "application/json"
        Write-Host "Department Prediction:" -ForegroundColor Green
        $response | ConvertTo-Json
    }
    catch {
        Write-Host "Department Prediction Error: $_" -ForegroundColor Red
    }

    # Test Priority Prediction
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/predict_priority" -Method Post -Body $body -ContentType "application/json"
        Write-Host "Priority Prediction:" -ForegroundColor Green
        $response | ConvertTo-Json
    }
    catch {
        Write-Host "Priority Prediction Error: $_" -ForegroundColor Red
    }

    Write-Host "--------------------------------"
}