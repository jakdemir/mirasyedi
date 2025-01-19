import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SpouseForm from './components/forms/SpouseForm';
import ChildrenForm from './components/forms/ChildrenForm';
import ParentsForm from './components/forms/ParentsForm';
import GrandparentsForm from './components/forms/GrandparentsForm';
import Layout from './components/Layout';
import Footer from './components/Footer';
import { FamilyTreeProvider } from './context/FamilyTreeContext';

function App() {
  return (
    <FamilyTreeProvider>
      <Router>
        <div className="min-h-screen flex flex-col">
          <div className="flex-grow">
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<SpouseForm />} />
                <Route path="children" element={<ChildrenForm />} />
                <Route path="parents" element={<ParentsForm />} />
                <Route path="grandparents" element={<GrandparentsForm />} />
              </Route>
            </Routes>
          </div>
          <Footer />
        </div>
      </Router>
    </FamilyTreeProvider>
  );
}

export default App;
