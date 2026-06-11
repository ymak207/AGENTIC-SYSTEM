from tools.router import ToolRouter

router = ToolRouter()

result = router.route("What is 25 * (3 + 7)?")

print(result)