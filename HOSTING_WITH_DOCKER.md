# How to Host with Docker & CI/CD (Simple Explanation)

You asked about **Vercel** and **Netlify**. I have an important update for you:
> 🚫 **Vercel and Netlify are NOT good for Streamlit.** 
> They are designed for "static" websites (like a poster). Streamlit needs to be "running" constantly (like a machine).

Instead, you should use **Railway** or **Render**. They are perfect for Docker.

---

## 📦 What is this "Docker Image" thing?
Imagine you are baking a cake.
- **Your Code** is the *Recipe*.
- **Your Computer** is your *Kitchen*.
- **The Problem**: Sometimes the recipe fails in your friend's kitchen because they have a different oven or missing ingredients.

**Docker** solves this by putting the whole kitchen into a box.
- Start with a "Base Image" (Empty Kitchen).
- Add Python (Install the Oven).
- Add Requirements (Buy Ingredients).
- Add Code (The Recipe).

Now, you don't send the recipe. You send the **entire box** (The Docker Image). If it bakes in your box, it bakes everywhere.

---

## 🤖 What is CI/CD?
(Continuous Integration / Continuous Deployment)

Imagine a **Robot Butler** who watches your code.
1.  **You** save a file and push it to GitHub.
2.  **The Butler (CI)** sees the change. He immediately wakes up.
3.  He reads your Docker instructions.
4.  He builds a *brand new* Docker box with your new code.
5.  **The Butler (CD)** takes the old box off the internet and plugs in the new one.

You don't do anything. You just save your code, and the robot updates the website.

---

## 🚀 How to Host (Step-by-Step)
We will use **Railway.app** because it handles Docker + CI/CD automatically.

### Phase 1: The Code (GitHub)
1.  Make sure your project is on GitHub.
2.  Your project must have the `Dockerfile` inside (It already does!).

### Phase 2: The Host (Railway)
1.  Go to **Railway.app** and Login with GitHub.
2.  Click **New Project** -> **Deploy from GitHub repo**.
3.  Select your `influencerhub` repo.
4.  **Important**: Since you have two parts (Frontend & Backend), you need to add them separately.

#### Setting up Backend
1.  Click the simplified project view.
2.  Click **Settings** -> **Root Directory**: Set it to `/backend`.
3.  Railway will find the `Dockerfile` inside `/backend` and start building the "Box".
4.  Go to **Variables** and add your secrets (Start with `PORT` = `8000`).
5.  It will give you a domain (e.g., `backend-production.up.railway.app`).

#### Setting up Frontend
1.  Add a **New Service** (in the same project) -> GitHub Repo -> Same Repo.
2.  **Settings** -> **Root Directory**: Set it to `/frontend`.
3.  Railway finds `frontend/Dockerfile`.
4.  **Variables**: Add `API_URL` and paste the Backend URL you just got.
5.  It will give you a domain (e.g., `frontend-production.up.railway.app`).

### 🎉 The Result
Every time you `git push` code to GitHub:
1.  Railway (The Robot) sees it.
2.  It re-builds the Docker Image.
3.  It updates the website.
**That is CI/CD.**
