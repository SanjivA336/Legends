import AccountLayout from "@layouts/AccountLayout";
import SecurityForm from "@features/account/SecurityForm";

export default function AccountSecurityPage() {

    return (
        <AccountLayout>
            <div className="w-100 h-100 rounded-5 p-4 bg-dark text-start">
                <h1 className="text-light">Security Settings</h1>
                <SecurityForm />
            </div>
        </AccountLayout>
    );
}
