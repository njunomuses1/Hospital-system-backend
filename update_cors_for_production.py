"""
Helper script to update CORS settings for production
Run this after you get your Vercel URL
"""
import sys
import os

def update_cors(vercel_url):
    """Update CORS settings in .env file"""
    
    # Validate URL
    if not vercel_url.startswith('https://'):
        print("❌ Error: Vercel URL must start with https://")
        return False
    
    vercel_url = vercel_url.rstrip('/')
    
    print("=" * 60)
    print("🔗 Updating CORS Settings for Production")
    print("=" * 60)
    print(f"\n✅ Vercel URL: {vercel_url}")
    
    # Read current .env
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"\n❌ Error: {env_file} not found!")
        return False
    
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update or add CORS settings
    updated_lines = []
    found_frontend_url = False
    found_allowed_origins = False
    
    for line in lines:
        if line.startswith('FRONTEND_URL='):
            updated_lines.append(f'FRONTEND_URL={vercel_url}\n')
            found_frontend_url = True
        elif line.startswith('ALLOWED_ORIGINS='):
            # Allow both exact URL and preview deployments
            updated_lines.append(f'ALLOWED_ORIGINS={vercel_url},{vercel_url.replace("https://", "https://*.")}\n')
            found_allowed_origins = True
        else:
            updated_lines.append(line)
    
    # Add if not found
    if not found_frontend_url:
        updated_lines.append(f'\n# Production CORS\nFRONTEND_URL={vercel_url}\n')
    
    if not found_allowed_origins:
        updated_lines.append(f'ALLOWED_ORIGINS={vercel_url},{vercel_url.replace("https://", "https://*.")}\n')
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("\n✅ CORS settings updated in .env file!")
    print("\n📋 Updated settings:")
    print(f"   FRONTEND_URL={vercel_url}")
    print(f"   ALLOWED_ORIGINS={vercel_url},{vercel_url.replace('https://', 'https://*.')}")
    
    print("\n⚠️  Important: You need to update these in Railway Dashboard too!")
    print("\nSteps:")
    print("1. Go to Railway Dashboard → Your Backend Service")
    print("2. Click 'Variables' tab")
    print("3. Update these variables:")
    print(f"   - FRONTEND_URL = {vercel_url}")
    print(f"   - ALLOWED_ORIGINS = {vercel_url},{vercel_url.replace('https://', 'https://*.')}")
    print("4. Railway will auto-redeploy")
    print("5. Test your app!")
    
    return True

def main():
    print("\n" + "=" * 60)
    print("🚀 Production CORS Configuration Helper")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        vercel_url = sys.argv[1]
    else:
        print("\nEnter your Vercel URL (e.g., https://your-app.vercel.app)")
        vercel_url = input("Vercel URL: ").strip()
    
    if not vercel_url:
        print("\n❌ Error: No URL provided")
        print("\nUsage: python update_cors_for_production.py https://your-app.vercel.app")
        sys.exit(1)
    
    if update_cors(vercel_url):
        print("\n" + "=" * 60)
        print("✅ Configuration updated successfully!")
        print("=" * 60)
        print("\nNext: Update the same variables in Railway Dashboard")
        print("Then your app will be fully connected! 🎉")
    else:
        print("\n❌ Configuration update failed")
        sys.exit(1)

if __name__ == "__main__":
    main()









