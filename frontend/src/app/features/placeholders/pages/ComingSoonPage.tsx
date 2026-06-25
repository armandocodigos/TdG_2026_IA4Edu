export function ComingSoonPage({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex min-h-full items-center justify-center px-8 py-12">
      <div className="w-full max-w-2xl rounded-lg border border-[#e5e5e5] bg-white p-8">
        <h1 className="text-[24px] font-semibold text-[#171717]">{title}</h1>
        <p className="mt-3 text-[14px] leading-7 text-[#737373]">{description}</p>
        <p className="mt-6 text-[13px] leading-6 text-[#737373]">
          The frontend structure is already prepared for this module, but the backend still does not expose the required workflow.
        </p>
        <a
          href="/diagnostic"
          className="mt-6 inline-flex rounded-md bg-[#171717] px-4 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#404040]"
        >
          Back to available modules
        </a>
      </div>
    </div>
  );
}
