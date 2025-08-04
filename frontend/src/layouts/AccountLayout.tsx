import BaseLayout from "@/layouts/BaseLayout";
import AccountSidebar from "@components/AccountSidebar";

type AccountLayoutProps = {
    children: React.ReactNode;
};

export default function AccountLayout({ children }: AccountLayoutProps) {

    return (
        <BaseLayout>
            <div className="d-flex w-100 h-100">
                {/* Sidebar */}
                <div className="col-md-3 col-lg-2 mt-4">
                    <AccountSidebar />
                </div>

                {/* Main Content */}
                <div className="col-md-9 col-lg-10">
                    {children}
                </div>
            </div>
        </BaseLayout>
    );
}
