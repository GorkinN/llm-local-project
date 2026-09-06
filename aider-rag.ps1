# aider-rag.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [Parameter()]
    [string[]]$Files
)

$cmd = "python aider_rag.py `"$Query`""

if ($Files) {
    $cmd += " --files " + ($Files -join " ")
}

Invoke-Expression $cmd