# SQLi Scanner - Usage Guide

This document provides detailed instructions on how to use the SQLi Scanner application, including explanations of all available options and recommended practices.

## Getting Started

After installing and setting up the application as described in the README and INSTALLATION guide, you can access the web interface by opening your browser and navigating to:
```
http://localhost:5000
```

## Scanner Interface Overview

The scanner interface is divided into several sections:

1. **Target Selection**
2. **Basic Options**
3. **Detection Options**
4. **Injection Options**
5. **Request Options**
6. **Enumeration Options**
7. **Advanced Options**

## Target Selection

### Target Type

- **Specific URL**: Use this option to scan a single URL with parameters. This is useful when you want to test a specific page that you suspect might be vulnerable.
  - Example: `https://example.com/page.php?id=1`

- **Domain (Crawl and Scan)**: Use this option to automatically crawl a website and test all discovered URLs. This is useful for comprehensive testing of an entire website.
  - Example: `example.com`

## Scanning Options Explained

### Basic Options

- **Crawl Depth**: Determines how deep the crawler will go when exploring a website. Higher values will discover more pages but will take longer to complete.
  - Recommended: Start with 1-2 for initial testing

- **Test Forms**: When enabled, the scanner will automatically test HTML forms found on the website by submitting them with test payloads.

### Detection Options

- **Detection Level (--level)**: Controls the intensity of the tests.
  - Level 1: Tests only GET and POST parameters
  - Level 2: Adds cookie testing
  - Level 3: Adds User-Agent and Referer header testing
  - Level 4: Adds more HTTP headers testing
  - Level 5: Includes all tests and is the most thorough but slowest option
  - Recommended: Start with 1 or 2 for initial scans

- **Risk Level (--risk)**: Controls how dangerous the test payloads are.
  - Risk 1: Includes simple payloads with minimal risk of affecting the database
  - Risk 2: Includes more advanced payloads
  - Risk 3: Includes payloads that may cause issues on the target database
  - Recommended: Start with 1 for production systems

### Injection Options

- **SQL Injection Techniques**: Specifies which techniques to use during testing.
  - B: Boolean-based blind SQL injection
  - E: Error-based SQL injection
  - U: Union query-based SQL injection
  - S: Stacked queries SQL injection
  - T: Time-based blind SQL injection
  - Q: Inline queries SQL injection
  - Recommended: Start with B,E for faster scans

- **Tamper Scripts**: Allows specifying SQLMap tamper scripts to evade WAF/IPS protection.
  - Example: `space2comment,between,charencode`
  - Use when the target has security measures that block standard SQL injection attempts

### Request Options

- **HTTP POST Data**: Data to be sent with POST requests.
  - Format: `param1=value1&param2=value2`

- **Cookie**: HTTP cookies to include with requests.
  - Format: `name1=value1; name2=value2`
  - Useful for testing authenticated areas of a website

- **User-Agent**: Custom User-Agent string to use for HTTP requests.
  - Example: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`

### Enumeration Options

- **Enumerate DBs**: When a SQL injection is found, attempt to retrieve database names.

- **Enumerate Tables**: When a SQL injection is found, attempt to retrieve table names.

- **Enumerate Columns**: When a SQL injection is found, attempt to retrieve column names.

### Advanced Options

- **Threads**: Number of concurrent threads to use during testing.
  - Higher values speed up scanning but may overload the target server
  - Recommended: 3-5 for most systems

- **Time Delay Seconds**: Seconds to wait for time-based blind SQL injections.
  - Longer values increase reliability for slow connections but extend scan time

- **Timeout**: Seconds to wait before timing out HTTP requests.
  - Increase for slower connections

- **Batch Mode**: Never ask for user input, use the default answer for all questions.
  - Recommended: Keep enabled for automated scanning

- **Random User-Agent**: Use a random User-Agent for each request.
  - Helps avoid detection by WAF/IPS systems

- **Dump Database Data**: When a SQL injection is found, attempt to extract actual data from the database.
  - Use with caution as this extracts real data

- **Get OS Shell**: Attempt to get an operating system shell if the vulnerability allows it.
  - Use with extreme caution and only on systems you own

- **Check for DBA Privileges**: Check if the database user has DBA (administrator) privileges.

- **Enumerate Users/Passwords**: Attempt to extract database user accounts and password hashes.

- **Test All Features**: Comprehensive testing using all available options.
  - Longest scan time but most thorough

## Interpreting Results

The results page shows:

1. **Scan Information**:
   - Target URL/domain
   - Start and end time
   - Status of the scan

2. **Vulnerabilities Found**:
   - URL of the vulnerable page
   - Vulnerable parameter
   - Type of vulnerability
   - Detailed information about each finding

3. **Database Information** (if enumeration was enabled):
   - Database names
   - Table names
   - Column names
   - Extracted data (if dump was enabled)

## Recommended Scanning Approaches

### Quick Scan

For a quick initial test:
- Target Type: Specific URL
- Crawl Depth: 1
- Detection Level: 1
- Risk Level: 1
- Techniques: B,E
- Threads: 3

### Thorough Scan

For a comprehensive test:
- Target Type: Domain
- Crawl Depth: 3
- Detection Level: 3
- Risk Level: 2
- Techniques: B,E,U,T
- Threads: 3
- Enable: Enumerate DBs, Tables, Columns

### Security Audit

For a complete security audit:
- Target Type: Domain
- Crawl Depth: 5
- Detection Level: 5
- Risk Level: 3
- Techniques: B,E,U,S,T,Q
- Threads: 3
- Enable all enumeration options
- Enable: Dump Database Data, Check for DBA Privileges

## Security and Ethical Considerations

Always remember:
- Only scan websites you own or have explicit permission to test
- Be careful with high risk levels on production systems
- Use data dumping features ethically and legally
- Be mindful of scan intensity and thread count to prevent DoS-like effects
- Store found vulnerabilities securely and report them responsibly

## Troubleshooting Common Issues

### Scan Never Completes

- Reduce crawl depth
- Reduce detection level
- Use fewer techniques (B,E are fastest)
- Increase timeout values

### False Positives

- Verify findings manually
- Increase detection level for more accurate testing
- Try different techniques

### False Negatives

- Increase detection level
- Increase risk level
- Try additional techniques
- Test with WAF bypass (tamper scripts)

## Integrating with Security Workflows

This SQLi Scanner can be integrated into your security testing workflow:

1. **Initial Reconnaissance**: Use domain crawling to map the application
2. **Vulnerability Scanning**: Run targeted scans on discovered endpoints
3. **Verification**: Verify found vulnerabilities manually
4. **Remediation**: Fix vulnerabilities in your code
5. **Regression Testing**: Re-scan to verify fixes

## Additional Resources

- [SQLMap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)
- [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)