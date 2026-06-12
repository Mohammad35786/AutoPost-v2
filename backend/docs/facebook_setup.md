# Facebook App Setup Guide

This guide explains how to set up a Facebook App in Meta for Developers to enable Facebook Login and Page integration for AutoPoster.

## 1. Create a Facebook App
1. Go to [Meta for Developers](https://developers.facebook.com/) and log in with your Facebook account.
2. Click on **My Apps** in the top right corner.
3. Click the **Create App** button.
4. Select **Other** as the use case, then click **Next**.
5. Select **Business** as the app type, then click **Next**.
6. Fill in the **App Name** (e.g., "AutoPoster App"), your **App Contact Email**, and optionally select a Business Account.
7. Click **Create App** and complete the security check if prompted.

## 2. Add Facebook Login Product
1. In your App Dashboard, scroll down to the **Add products to your app** section.
2. Find **Facebook Login for Business** (or just **Facebook Login**) and click **Set Up**.
3. Choose **Web** as the platform.
4. For the Site URL, enter your frontend URL (e.g., `http://localhost:5173` or your production domain), then save and continue.

## 3. Configure Facebook Login Settings
1. In the left sidebar, under **Facebook Login**, click on **Settings**.
2. Find the **Valid OAuth Redirect URIs** field.
3. Enter your callback URL. It should be: `{BACKEND_URL}/facebook/callback` (Replace `{BACKEND_URL}` with your actual backend URL, e.g., `http://localhost:8000/facebook/callback`).
4. Click **Save Changes** at the bottom of the page.

## 4. Get App ID and App Secret
1. In the left sidebar, expand **App Settings** and click on **Basic**.
2. Here you will find your **App ID** and **App Secret** (click "Show" to reveal the secret).
3. Copy these values and paste them into your `.env` file as `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET`.

## 5. Required Permissions / Scopes
When a user logs in, the app will request the following permissions to function correctly:
- `pages_show_list`: To fetch the list of Facebook Pages the user manages.
- `pages_read_engagement`: To read engagement metrics and details about the Pages.
- `pages_manage_posts`: To allow the app to publish and manage posts on the user's Pages.

*(Note: During development, you can use these permissions freely with accounts holding a role in the app. For production, these permissions will require App Review by Facebook.)*
