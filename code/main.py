from code.graphs.pi_team_leader import graph

if __name__ == "__main__":
    # Inputs
    source_text = """to PLMs, LLMs are not only much larger in model size, but
    also exhibit stronger language understanding and generation
    abilities, and more importantly, emergent abilities that are
    not present in smaller-scale language models. As illustrated
    in Fig. 1, these emergent abilities include (1) in-context
    learning, where LLMs learn a new task from a small set
    of examples presented in the prompt at inference time, (2)
    instruction following, where LLMs, after instruction tuning."""
    thread = {"configurable": {"thread_id": "1"}}

    # Run the graph with the example text
    for event in graph.stream({"source_text": source_text},
                              thread,
                              stream_mode="updates"):
        print("--Node--")
        node_name = next(iter(event.keys()))
        print(node_name)
    final_state = graph.get_state(thread)
    report = final_state.values.get('final_report')
    print(report)