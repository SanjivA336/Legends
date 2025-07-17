import BaseLayout from "@/layouts/BaseLayout";

export default function HomePage() {

    return (
        <BaseLayout>
            <div className="d-flex flex-column gap-5 w-100 h-auto">
                {/* Hero Section */}
                <div className="w-100 vh-100 align-content-center text-center">
                    <div className="w-100 d-flex text-center justify-content-center">
                        <h1 className="text-light" style={{ fontSize: "5rem" }}>Welcome to&nbsp;</h1>
                        <h1 className="text-primary" style={{ fontSize: "5rem" }}>Legends.</h1>
                    </div>
                    <div className="w-100 d-flex text-center justify-content-center">
                        <h1 className="text-light">Write</h1>
                        <h1 className="text-primary">&nbsp;Your&nbsp;</h1>
                        <h1 className="text-light">Story.</h1>
                    </div>
                </div>

                {/* Library Section */}
                <div className="w-100 d-flex flex-column align-items-start justify-content-center bg-dark text-light p-5 rounded-5">
                    <h1 className="text-light">Your Library</h1>

                </div>
            </div>
        </BaseLayout>
    );
}
