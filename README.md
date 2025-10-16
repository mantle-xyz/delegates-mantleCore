# Delegates MantleCore

This repository manages delegate data for MantleCore, featuring automated data validation and merge rules.

## 📋 Project Structure

```
delegates-mantleCore/
├── delegates.json              # Delegate data file
├── .github/
│   └── workflows/
│       └── validate-delegates.yml  # Automated validation workflow
└── README.md                   # Project documentation
```

## 🔍 Data Format

The `delegates.json` file contains an array of delegate information. Each delegate object must include the following fields:

### Required Fields

- **Voteweight**: Voting weight (numeric type, must be ≥ 0)
- **Address**: Ethereum address (string type, must be a valid Ethereum address format)

### Optional Fields

- **InternalReference**: Internal reference (string type)

### Example

```json
[
  {
    "Voteweight": 100,
    "Address": "0xC8889f2a2d36eD0BBa88443F11791714b0971843",
    "InternalReference": "test 1"
  },
  {
    "Voteweight": 15,
    "Address": "0xE4459c2c76B0CDFD33DE8a2635157c248a4DEeB7",
    "InternalReference": "test 2"
  }
]
```

## ✅ Validation Rules

### 1. Field Validation
- **Voteweight**: Must be a numeric type and greater than or equal to 0
- **Address**: Must be a valid Ethereum address format

### 2. Ethereum Address Format
- Must start with `0x` (optional, will be added automatically)
- Followed by 40 hexadecimal characters (0-9, a-f, A-F)
- Total length of 42 characters
- Example: `0x1234567890123456789012345678901234567890`

### 3. JSON Format
- Must be valid JSON format
- Root element must be an array
- Each array element must be an object

## 🚀 Automated Validation

### GitHub Actions Workflow

The project uses GitHub Actions for automated validation:

- **Trigger Conditions**: Push to main branch or create Pull Request
- **Validation Content**: 
  - JSON format validation
  - Required field checks
  - Ethereum address format validation
- **PR Comments**: Automatically displays validation results in Pull Request

### Workflow File

Validation logic is directly written in `.github/workflows/validate-delegates.yml`, requiring no additional validation scripts.

## 🛠️ Local Validation

If you need to validate data format locally, you can use the following Python code:

```bash
python3 << 'EOF'
import json
import re

def validate_ethereum_address(address):
    if not isinstance(address, str):
        return False, "Address must be a string type"
    if not re.match(r'^(0x)?[0-9a-fA-F]{40}$', address):
        return False, "Invalid address format"
    if not address.startswith('0x'):
        address = '0x' + address
    return True, address

with open('delegates.json', 'r') as f:
    delegates = json.load(f)

for i, delegate in enumerate(delegates):
    if 'Voteweight' not in delegate:
        print(f"❌ Delegate {i+1} missing Voteweight field")
    if 'Address' not in delegate:
        print(f"❌ Delegate {i+1} missing Address field")
    else:
        valid, result = validate_ethereum_address(delegate['Address'])
        if not valid:
            print(f"❌ Delegate {i+1} invalid address: {result}")

print("✅ Validation completed")
EOF
```

## 📝 Usage Instructions

### Adding New Delegates

1. Edit the `delegates.json` file
2. Add new delegate objects, ensuring required fields are included
3. Commit changes and push to the repository
4. GitHub Actions will automatically validate the data format

### Modifying Existing Delegates

1. Edit the `delegates.json` file
2. Modify the corresponding delegate information
3. Commit changes
4. Validation will run automatically

### Pull Request Process

1. Create a Pull Request
2. GitHub Actions automatically validates
3. Check validation results in PR comments
4. If validation passes, you can merge to main branch

## ⚠️ Important Notes

- Ensure all addresses are in valid Ethereum address format
- Voteweight must be a numeric type, not a string
- JSON format must be correct, recommend using a JSON-supporting editor
- Suggest performing local validation before committing

## 🔧 Troubleshooting

### Common Errors

1. **JSON Format Error**: Check if JSON syntax is correct
2. **Missing Required Fields**: Ensure each delegate includes Voteweight and Address
3. **Address Format Error**: Ensure address starts with 0x followed by 40 hexadecimal characters
4. **Data Type Error**: Voteweight must be a number, not a string

### Getting Help

If you encounter issues, please check:
1. GitHub Actions validation logs
2. Validation comments in Pull Request
3. Local validation output results

## 📄 License

This project follows the corresponding open source license.
