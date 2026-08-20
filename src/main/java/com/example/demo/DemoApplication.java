package com.example.demo; // 🟢 메인 파일은 항상 모든 폴더를 품을 수 있는 최상단에!

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;

// 1. 이 어노테이션이 바로 사장님의 "레이더"입니다.
@SpringBootApplication
@Controller
public class DemoApplication {
	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}
}