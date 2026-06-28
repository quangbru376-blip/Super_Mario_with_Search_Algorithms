import re

with open(r'c:\Study\AI\Final_project_pygame\algorithms\complex_env.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace states.append({ with yield {
content = content.replace("states.append({", "yield {")

# Replace }) with } for the ends of those dicts
content = re.sub(r'    }\)', r'    }', content)
content = re.sub(r'        }\)', r'        }', content)

# Remove states = []
content = content.replace("    states = []\n", "")

# Remove return states
content = content.replace("    return states", "")
content = content.replace("        return states", "        return")

with open(r'c:\Study\AI\Final_project_pygame\algorithms\complex_env.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Refactored complex_env.py")
