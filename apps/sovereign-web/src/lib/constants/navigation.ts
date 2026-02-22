import {
    Activity,
    ArrowLeftRight,
    DollarSign,
    Shield,
    Briefcase,
    Car,
    Camera,
    Search,
    Lightbulb,
    Brain,
    History,
} from "lucide-svelte";

export const coreTabs = [
    { id: "overview", name: "OVERVIEW", icon: Activity },
    { id: "transfers", name: "TRANSFERS", icon: ArrowLeftRight },
    { id: "wallet", name: "WALLET", icon: DollarSign },
    { id: "command", name: "CENTRAL COMMAND", icon: Shield },
    { id: "wellbeing", name: "WELLBEING", icon: Brain },
];

export const ecosystemTabs = [
    { id: "market", name: "MARKETPLACE", icon: Briefcase },
    { id: "mobility", name: "MOBILITY", icon: Car },
    { id: "stories", name: "MOMENTS", icon: History },
    { id: "cinema", name: "SOVEREIGN CINEMA", icon: Camera },
    { id: "forensics", name: "WITR FORENSICS", icon: Search },
    { id: "strategies", name: "STRATEGY FEED", icon: Lightbulb },
];
