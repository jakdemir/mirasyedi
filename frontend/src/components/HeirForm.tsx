import React, { useState } from 'react';
import { Heir, RelationType, FamilyBranch, ParentType } from '../types';

interface HeirFormProps {
    onAdd: (heir: Heir) => void;
    existingSpouse: boolean;
    hasChildren: boolean;
    hasParents: boolean;
}

type Step = 'spouse' | 'first-degree' | 'second-degree' | 'third-degree';

const RELATION_TYPES = {
    SPOUSE: 'spouse' as RelationType,
    CHILD: 'child' as RelationType,
    PARENT: 'parent' as RelationType,
    GRANDPARENT: 'grandparent' as RelationType
} as const;

export const HeirForm: React.FC<HeirFormProps> = ({ onAdd, existingSpouse, hasChildren, hasParents }) => {
    const [currentStep, setCurrentStep] = useState<Step>('spouse');
    const [name, setName] = useState('');
    const [relation, setRelation] = useState<RelationType>(RELATION_TYPES.SPOUSE);
    const [isAlive, setIsAlive] = useState(true);
    const [branch, setBranch] = useState<FamilyBranch | undefined>(undefined);
    const [parentType, setParentType] = useState<ParentType | undefined>(undefined);
    const [children, setChildren] = useState<Heir[]>([]);
    const [childName, setChildName] = useState('');
    const [childIsAlive, setChildIsAlive] = useState(true);
    const [childrenOfChild, setChildrenOfChild] = useState<Heir[]>([]);
    const [childOfChildName, setChildOfChildName] = useState('');

    // Determine available steps based on inheritance rules
    const availableSteps: Step[] = ['spouse'];
    if (!hasChildren) {
        availableSteps.push('first-degree');
        if (!hasParents) {
            availableSteps.push('second-degree');
            availableSteps.push('third-degree');
        }
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const heir: Heir = {
            id: `${name}-${Date.now()}`,
            name,
            relation: currentStep === 'spouse' ? RELATION_TYPES.SPOUSE :
                     currentStep === 'first-degree' ? RELATION_TYPES.CHILD :
                     currentStep === 'second-degree' ? RELATION_TYPES.PARENT :
                     RELATION_TYPES.GRANDPARENT,
            is_alive: isAlive,
            branch: currentStep === 'third-degree' ? branch : undefined,
            parent_type: currentStep === 'second-degree' ? parentType : undefined,
            children: !isAlive ? children : undefined,
            share: undefined
        };
        onAdd(heir);

        // Only reset form completely if not adding children or parents
        if (currentStep === 'first-degree' || currentStep === 'second-degree' || currentStep === 'third-degree') {
            // Just reset the name field to allow adding more heirs
            setName('');
            setIsAlive(true);
            setChildren([]);
            if (currentStep === 'second-degree') {
                setParentType(undefined);
            }
        } else {
            resetForm();
        }
    };

    const handleAddChild = () => {
        if (childName.trim()) {
            const child: Heir = {
                id: `${childName}-${Date.now()}`,
                name: childName,
                relation: currentStep === 'first-degree' ? RELATION_TYPES.CHILD :
                         currentStep === 'second-degree' ? RELATION_TYPES.PARENT :
                         RELATION_TYPES.GRANDPARENT,
                is_alive: childIsAlive,
                children: !childIsAlive ? childrenOfChild : undefined,
                branch: currentStep === 'second-degree' || currentStep === 'third-degree' ? branch : undefined,
                share: undefined
            };
            setChildren([...children, child]);
            setChildName('');
            setChildIsAlive(true);
            setChildrenOfChild([]);
        }
    };

    const handleAddChildOfChild = () => {
        if (childOfChildName.trim()) {
            const child: Heir = {
                id: `${childOfChildName}-${Date.now()}`,
                name: childOfChildName,
                relation: currentStep === 'first-degree' ? RELATION_TYPES.CHILD :
                         currentStep === 'second-degree' ? RELATION_TYPES.PARENT :
                         RELATION_TYPES.GRANDPARENT,
                is_alive: true,
                branch: currentStep === 'second-degree' || currentStep === 'third-degree' ? branch : undefined,
                share: undefined
            };
            setChildrenOfChild([...childrenOfChild, child]);
            setChildOfChildName('');
        }
    };

    const handleRemoveChild = (childName: string) => {
        setChildren(children.filter(child => child.name !== childName));
    };

    const handleRemoveChildOfChild = (childName: string) => {
        setChildrenOfChild(childrenOfChild.filter(child => child.name !== childName));
    };

    const resetForm = () => {
        setName('');
        setIsAlive(true);
        setBranch(undefined);
        setParentType(undefined);
        setChildren([]);
        setChildName('');
        setChildIsAlive(true);
        setChildrenOfChild([]);
        setChildOfChildName('');

        // Move to next available step
        const currentIndex = availableSteps.indexOf(currentStep);
        if (currentIndex < availableSteps.length - 1) {
            const nextStep = availableSteps[currentIndex + 1];
            setCurrentStep(nextStep);
            switch (nextStep) {
                case 'first-degree':
                    setRelation(RELATION_TYPES.CHILD);
                    break;
                case 'second-degree':
                    setRelation(RELATION_TYPES.PARENT);
                    break;
                case 'third-degree':
                    setRelation(RELATION_TYPES.GRANDPARENT);
                    break;
                default:
                    setRelation(RELATION_TYPES.SPOUSE);
            }
        }
    };

    const getStepTitle = () => {
        switch (currentStep) {
            case 'spouse':
                return 'Step 1: Add Spouse';
            case 'first-degree':
                return 'Step 2: Add Children';
            case 'second-degree':
                return 'Step 3: Add Parents';
            case 'third-degree':
                return 'Step 4: Add Grandparents';
            default:
                return '';
        }
    };

    const getStepDescription = () => {
        switch (currentStep) {
            case 'spouse':
                return 'Start by adding the spouse (if any).';
            case 'first-degree':
                return 'Add children of the deceased. You can add multiple children, and for deceased children, you can add their children.';
            case 'second-degree':
                return 'Add parents if there are no children. Specify maternal or paternal.';
            case 'third-degree':
                return 'Add grandparents if there are no closer heirs. Specify maternal or paternal side.';
            default:
                return '';
        }
    };

    const getSubmitButtonText = () => {
        switch (currentStep) {
            case 'spouse':
                return 'Add Spouse';
            case 'first-degree':
                return 'Add Child';
            case 'second-degree':
                return 'Add Parent';
            case 'third-degree':
                return 'Add Grandparent';
            default:
                return 'Add Heir';
        }
    };

    const showSkipButton = (step: Step) => {
        switch (step) {
            case 'spouse':
                return !existingSpouse;
            case 'first-degree':
                return !hasChildren;
            case 'second-degree':
                return !hasParents;
            case 'third-degree':
                return false; // Last step, no skip button needed
            default:
                return false;
        }
    };

    // Don't show the form if spouse already exists and we're on the spouse step
    if (currentStep === 'spouse' && existingSpouse) {
        return (
            <div className="bg-white p-4 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Spouse Already Added</h3>
                <p className="mt-2 text-sm text-gray-600">
                    A spouse has already been added. You can proceed to add other family members.
                </p>
                <button
                    type="button"
                    onClick={() => setCurrentStep('first-degree')}
                    className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                    Continue to Children
                </button>
            </div>
        );
    }

    // Don't show the form if children exist and we're not on the first-degree step
    if (hasChildren && currentStep !== 'first-degree') {
        return (
            <div className="bg-white p-4 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Children Already Added</h3>
                <p className="mt-2 text-sm text-gray-600">
                    Since there are children in the family tree, you can only add more children. Parents and grandparents cannot inherit when there are children.
                </p>
                <button
                    type="button"
                    onClick={() => setCurrentStep('first-degree')}
                    className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                    Add More Children
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="text-lg font-medium text-gray-900">{getStepTitle()}</h3>
                        <p className="mt-1 text-sm text-gray-600">{getStepDescription()}</p>
                    </div>
                    {!hasChildren && (
                        <div className="flex space-x-2">
                            {availableSteps.map((step, index) => (
                                <button
                                    key={step}
                                    type="button"
                                    onClick={() => {
                                        setCurrentStep(step);
                                        switch (step) {
                                            case 'spouse':
                                                setRelation(RELATION_TYPES.SPOUSE);
                                                break;
                                            case 'first-degree':
                                                setRelation(RELATION_TYPES.CHILD);
                                                break;
                                            case 'second-degree':
                                                setRelation(RELATION_TYPES.PARENT);
                                                break;
                                            case 'third-degree':
                                                setRelation(RELATION_TYPES.GRANDPARENT);
                                                break;
                                        }
                                    }}
                                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                                        currentStep === step ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:text-gray-700'
                                    }`}
                                >
                                    {index + 1}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg border border-gray-200">
                <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                        Name
                    </label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        placeholder="Enter name"
                    />
                </div>

                <div>
                    <div className="flex items-center">
                        <input
                            type="checkbox"
                            id="isAlive"
                            checked={isAlive}
                            onChange={(e) => setIsAlive(e.target.checked)}
                            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        />
                        <label htmlFor="isAlive" className="ml-2 block text-sm text-gray-900">
                            Is Alive
                        </label>
                    </div>
                </div>

                {currentStep === 'second-degree' && (
                    <div>
                        <label htmlFor="parentType" className="block text-sm font-medium text-gray-700">
                            Parent Type
                        </label>
                        <select
                            id="parentType"
                            value={parentType || ''}
                            onChange={(e) => setParentType(e.target.value ? e.target.value as ParentType : undefined)}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        >
                            <option value="">Select parent type</option>
                            <option value={ParentType.MOTHER}>Mother</option>
                            <option value={ParentType.FATHER}>Father</option>
                        </select>
                    </div>
                )}

                {currentStep === 'third-degree' && (
                    <div>
                        <label htmlFor="branch" className="block text-sm font-medium text-gray-700">
                            Branch
                        </label>
                        <select
                            id="branch"
                            value={branch || ''}
                            onChange={(e) => setBranch(e.target.value ? e.target.value as FamilyBranch : undefined)}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        >
                            <option value="">Select branch</option>
                            <option value={FamilyBranch.MATERNAL}>Maternal</option>
                            <option value={FamilyBranch.PATERNAL}>Paternal</option>
                        </select>
                    </div>
                )}

                {!isAlive && (currentStep === 'first-degree' || currentStep === 'second-degree' || currentStep === 'third-degree') && (
                    <div className="space-y-4">
                        <div className="bg-gray-50 p-4 rounded-md">
                            <h4 className="text-sm font-medium text-gray-900 mb-2">
                                {currentStep === 'first-degree' ? "Add Children" :
                                 currentStep === 'second-degree' ? "Add Parent's Children" :
                                 "Add Grandparent's Children"}
                            </h4>
                            <div className="space-y-4">
                                <div>
                                    <label htmlFor="childName" className="block text-sm font-medium text-gray-700">
                                        {currentStep === 'first-degree' ? "Child's Name" :
                                         currentStep === 'second-degree' ? "Sibling's Name" :
                                         "Aunt/Uncle's Name"}
                                    </label>
                                    <div className="mt-1 flex gap-2">
                                        <input
                                            type="text"
                                            id="childName"
                                            value={childName}
                                            onChange={(e) => setChildName(e.target.value)}
                                            placeholder={currentStep === 'first-degree' ? "Enter child's name" :
                                                       currentStep === 'second-degree' ? "Enter sibling's name" :
                                                       "Enter aunt/uncle's name"}
                                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex items-center">
                                        <input
                                            type="checkbox"
                                            id="childIsAlive"
                                            checked={childIsAlive}
                                            onChange={(e) => setChildIsAlive(e.target.checked)}
                                            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                                        />
                                        <label htmlFor="childIsAlive" className="ml-2 block text-sm text-gray-900">
                                            {currentStep === 'first-degree' ? "Child Is Alive" :
                                             currentStep === 'second-degree' ? "Sibling Is Alive" :
                                             "Aunt/Uncle Is Alive"}
                                        </label>
                                    </div>
                                </div>
                                {!childIsAlive && (
                                    <div className="mt-4 pl-4 border-l-2 border-gray-200">
                                        <h5 className="text-sm font-medium text-gray-900 mb-2">
                                            {currentStep === 'first-degree' ? "Add Child's Children" :
                                             currentStep === 'second-degree' ? "Add Sibling's Children" :
                                             "Add Aunt/Uncle's Children"}
                                        </h5>
                                        <div className="space-y-2">
                                            <div className="flex gap-2">
                                                <input
                                                    type="text"
                                                    value={childOfChildName}
                                                    onChange={(e) => setChildOfChildName(e.target.value)}
                                                    placeholder={currentStep === 'first-degree' ? "Enter grandchild's name" :
                                                               currentStep === 'second-degree' ? "Enter niece/nephew's name" :
                                                               "Enter cousin's name"}
                                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                                />
                                                <button
                                                    type="button"
                                                    onClick={handleAddChildOfChild}
                                                    className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                                >
                                                    Add
                                                </button>
                                            </div>
                                            {childrenOfChild.length > 0 && (
                                                <ul className="mt-2 space-y-1">
                                                    {childrenOfChild.map((child, index) => (
                                                        <li key={index} className="flex justify-between items-center text-sm text-gray-600">
                                                            <span>{child.name}</span>
                                                            <button
                                                                type="button"
                                                                onClick={() => handleRemoveChildOfChild(child.name)}
                                                                className="text-red-600 hover:text-red-800"
                                                            >
                                                                Remove
                                                            </button>
                                                        </li>
                                                    ))}
                                                </ul>
                                            )}
                                        </div>
                                    </div>
                                )}
                                <div className="flex justify-end">
                                    <button
                                        type="button"
                                        onClick={handleAddChild}
                                        className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        {currentStep === 'first-degree' ? "Add Child" :
                                         currentStep === 'second-degree' ? "Add Sibling" :
                                         "Add Aunt/Uncle"}
                                    </button>
                                </div>
                            </div>
                            {children.length > 0 && (
                                <div className="mt-4">
                                    <h5 className="text-sm font-medium text-gray-700 mb-2">Added Children:</h5>
                                    <ul className="space-y-2">
                                        {children.map((child, index) => (
                                            <li key={index} className="bg-white p-2 rounded border border-gray-200">
                                                <div className="flex justify-between items-start">
                                                    <div>
                                                        <div className="font-medium">{child.name}</div>
                                                        <div className="text-sm text-gray-500">
                                                            {child.is_alive ? 'Alive' : 'Deceased'}
                                                            {!child.is_alive && child.children && ` • ${child.children.length} Children`}
                                                        </div>
                                                        {!child.is_alive && child.children && child.children.length > 0 && (
                                                            <ul className="mt-1 pl-4 space-y-1">
                                                                {child.children.map((grandchild, gIndex) => (
                                                                    <li key={gIndex} className="text-sm text-gray-600">
                                                                        {grandchild.name}
                                                                    </li>
                                                                ))}
                                                            </ul>
                                                        )}
                                                    </div>
                                                    <button
                                                        type="button"
                                                        onClick={() => handleRemoveChild(child.name)}
                                                        className="text-red-600 hover:text-red-800"
                                                    >
                                                        Remove
                                                    </button>
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                <div className="flex justify-between">
                    {!hasChildren && (
                        <button
                            type="button"
                            onClick={() => {
                                const currentIndex = availableSteps.indexOf(currentStep);
                                if (currentIndex > 0) {
                                    const prevStep = availableSteps[currentIndex - 1];
                                    setCurrentStep(prevStep);
                                    switch (prevStep) {
                                        case 'spouse':
                                            setRelation(RELATION_TYPES.SPOUSE);
                                            break;
                                        case 'first-degree':
                                            setRelation(RELATION_TYPES.CHILD);
                                            break;
                                        case 'second-degree':
                                            setRelation(RELATION_TYPES.PARENT);
                                            break;
                                        case 'third-degree':
                                            setRelation(RELATION_TYPES.GRANDPARENT);
                                            break;
                                    }
                                }
                            }}
                            className={`inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 ${
                                availableSteps.indexOf(currentStep) === 0 ? 'invisible' : ''
                            }`}
                        >
                            Previous Step
                        </button>
                    )}
                    <div className="flex space-x-3">
                        {showSkipButton(currentStep) && (
                            <button
                                type="button"
                                onClick={() => {
                                    const currentIndex = availableSteps.indexOf(currentStep);
                                    if (currentIndex < availableSteps.length - 1) {
                                        const nextStep = availableSteps[currentIndex + 1];
                                        setCurrentStep(nextStep);
                                        switch (nextStep) {
                                            case 'first-degree':
                                                setRelation(RELATION_TYPES.CHILD);
                                                break;
                                            case 'second-degree':
                                                setRelation(RELATION_TYPES.PARENT);
                                                break;
                                            case 'third-degree':
                                                setRelation(RELATION_TYPES.GRANDPARENT);
                                                break;
                                        }
                                    }
                                }}
                                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                            >
                                Skip to Next Step
                            </button>
                        )}
                        <button
                            type="submit"
                            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        >
                            {getSubmitButtonText()}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
}; 