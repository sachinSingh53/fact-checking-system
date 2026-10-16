export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-zinc-50 px-6 py-20 dark:bg-zinc-950">
      <section className="w-full max-w-3xl rounded-3xl border border-zinc-200 bg-white p-10 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-14">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-700 dark:text-blue-400">
          Fact Checking System
        </p>
        <h1 className="mt-5 text-4xl font-semibold tracking-tight text-zinc-950 dark:text-white sm:text-5xl">
          Frontend foundation is ready.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-600 dark:text-zinc-300">
          The article submission, progress, and report experiences will be built
          here after their product contracts are approved.
        </p>
      </section>
    </main>
  );
}
