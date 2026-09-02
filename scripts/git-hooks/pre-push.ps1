$protectedFile = "vocabulary-trainer-web/public/preload-vocabulary.js"
$zeroSha = "0000000000000000000000000000000000000000"

foreach ($line in [Console]::In.ReadToEnd().Trim() -split "`n") {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    $localRef, $localSha, $remoteRef, $remoteSha = $line.Trim() -split "\s+"
    if ($remoteRef -eq "refs/heads/main" -or $remoteRef -notlike "refs/heads/*") {
        continue
    }

    if ($remoteSha -eq $zeroSha) {
        $changedFiles = git diff --name-only "origin/main...$localSha"
    } else {
        $changedFiles = git diff --name-only $remoteSha $localSha
    }

    if ($changedFiles -contains $protectedFile) {
        Write-Error "Push blocked: vocabulary updates must be deployed through main."
        Write-Error 'Run: .\deploy.ps1 -Message "Describe the vocabulary update"'
        exit 1
    }
}