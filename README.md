# Delegates Repository

This repository manages delegate data for the organization, featuring automated validation, merge rules, and synchronization workflows to ensure data integrity across multiple sources.

## 📋 Project Structure

```text
delegates-xxx/
├── delegates.json              # Delegate data file
├── .github/
│   ├── delegates-limits.json   # Repository-specific validation limits
│   ├── scripts/
│   │   └── validate_delegates.py   # Validation script
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

## ⚙️ Validation Limits

Repository-specific validation limits live in `.github/delegates-limits.json`.

- **max_total**: Required. Maximum total Voteweight allowed in the repository.
- **max_per_delegate**: Optional. Maximum Voteweight allowed per delegate.

Example:

```json
{
  "max_total": 1000,
  "max_per_delegate": 100
}
```

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
- **Watched Files**: `delegates.json`, `.github/delegates-limits.json`, validation script, workflow file
- **Validation Content**: 
  - JSON format validation
  - Required field checks
  - Ethereum address format validation
  - Repository-specific max total Voteweight limit
  - Optional per-delegate Voteweight limit
- **PR Comments**: Automatically displays validation results in Pull Request

### Workflow File

Workflow orchestration lives in `.github/workflows/validate-delegates.yml`, and the validation logic lives in `.github/scripts/validate_delegates.py`.

## 🛠️ Local Validation

If you need to validate data format locally, run:

```bash
python3 .github/scripts/validate_delegates.py
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
- `max_total` must be configured in `.github/delegates-limits.json`
- `max_per_delegate` is optional and only enforced when present
- JSON format must be correct, recommend using a JSON-supporting editor
- Suggest performing local validation before committing

## 🔧 Troubleshooting

### Common Errors

1. **JSON Format Error**: Check if JSON syntax is correct
2. **Missing Required Fields**: Ensure each delegate includes Voteweight and Address
3. **Address Format Error**: Ensure address starts with 0x followed by 40 hexadecimal characters
4. **Data Type Error**: Voteweight must be a number, not a string
5. **Limit Configuration Error**: Ensure `.github/delegates-limits.json` includes a valid `max_total`

### Getting Help

If you encounter issues, please check:
1. GitHub Actions validation logs
2. Validation comments in Pull Request
3. Local validation output results

## 📄 License

This project follows the corresponding open source license.
