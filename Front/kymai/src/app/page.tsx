export default function Home() {
    return (
        <div className="grid grid-rows-[20px_1fr_200px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-custom-bg">
            <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
                <div className="border-2 border-neutral-400 bg-neutral-400 p-4">
                    <h1 className="text-6xl font-bold text-white text-center sm:text-left whitespace-nowrap">
                        Welcome to Know Your Mood AI!
                    </h1>
                </div>
                <div className="border-2 border-neutral-400 bg-neutral-400 p-4">
                    <p className="text-2xl text-white text-center sm:text-left">
                        KYMAI is a platform when you can recognize your emotion from photo.
                    </p>
                </div>
            </main>
        </div>
    );
}
