import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

const Layout = () => {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex-grow container mx-auto max-w-5xl py-12 px-4">
                <Outlet />
            </main>
            <Footer />
        </div>
    );
};

export default Layout;